from collections import namedtuple

from BabuDuckError import BabyDuckError
from BabyDuckParser import BabyDuckParser
from BabyDuckVisitor import BabyDuckVisitor

from semantic_cube import semantic_cube
from symbol import Symbol, FuncInfo, SymbolTableManager

class SemanticVisitor(BabyDuckVisitor):
    def __init__(self):
        self.cube = semantic_cube
        self.table_manager = SymbolTableManager()        
        self.current_func_info = None # funcion actual para conocer los parámetros

        self.quadruples = []        
        self.operand_stack = [] 
        self.type_stack = []    
        self.operator_stack = []
        self.jump_stack = []
        self.temp_counter = 1
        self.pending_jump = None

    def _get_op_string(self, token_type):
	    """ 
        Helper function, no es un punto neurálgico
        Convierte un token de ANTLR a un string de operador
        """

	    op_map = {
		    BabyDuckParser.MAS: "+", 
            BabyDuckParser.MENOS: "-",
		    BabyDuckParser.MULTIPLICACION: "*", 
            BabyDuckParser.DIVISION: "/",
		    BabyDuckParser.MAYOR_QUE: ">", 
            BabyDuckParser.MENOR_QUE: "<",
		    BabyDuckParser.DIFERENTE_DE: "!=", 
            BabyDuckParser.IGUAL_QUE: "==",
		    BabyDuckParser.ASIGNACION: "="
		}

	    return op_map.get(token_type)

    def _validate_function_call(self, func_name, args_ctx_list, ctx_line):
        """
        Helper function, no es un punto neurálgico
        Valida una llamada a función usada en 2 puntos neurálgicos: `visitDato_o_llamada` y `visitEstatuto`
        1. Comprueba que la función exista.
        2. Comprueba el número de argumentos (aridad).
        3. Comprueba el tipo de cada argumento.
        Devuelve el tipo de retorno de la función.
        """
        # 1. Buscar la función (Error: Función no declarada)
        func_info = self.table_manager.lookup_function(func_name)
        if not func_info:
             # Chequeo extra por si era una variable usada como función
            if self.table_manager.lookup_variable(func_name):
                raise BabyDuckError("semantico", f"Uso incorrecto, '{func_name}' es una variable, no una función")
            else:
                raise BabyDuckError("semantico", f"Función '{func_name}' no declarada")
        
        # 2. Validar número de argumentos (Error: Conteo de argumentos)
        num_args_sent = len(args_ctx_list) if args_ctx_list else 0
        num_params_expected = len(func_info.param_types)
        
        if num_args_sent != num_params_expected:
            raise BabyDuckError("semantico", f"La función '{func_name}' esperaba {num_params_expected} parámetros, pero recibió {num_args_sent}")
            
        # 3. Validar tipo de cada argumento (Error: Mismatch en tipo de parámetro)
        for i in range(num_args_sent):
            arg_expr_ctx = args_ctx_list[i]
            arg_type = self.visit(arg_expr_ctx) # Visita la expresión del argumento
            
            expected_type = func_info.param_types[i]
            
            # Usar el cubo para checar compatibilidad (ej. asignar 'int' a 'float')
            check = self.cube[expected_type][arg_type].get('=')
            if check == 'error' or not check:
                raise BabyDuckError("semantico", f"Error en el parámetro {args_ctx_list[i]}: la función esperaba un parámetro de tipo {expected_type} pero se recibió {arg_type}")
        
        # 4. Devolver el tipo de retorno de la función
        return func_info.return_type

    def _generate_quad(self, operator, left_op, right_op, result):
        """
        Helper function, no es un punto neurálgico
        Crea un cuádruplo, lo agrega a la fila y devuelve su índice.
        """
        quad = Quadruple(operator, left_op, right_op, result)
        self.quadruples.append(quad)
        return len(self.quadruples) - 1

    # ===========================================================================
    # =============== Validar <PROGRAMA> y declaraciones globales ===============
    # ===========================================================================

    # 1. Inicializar el scope global en <PROGRAMA>
    def visitPrograma(self, ctx:BabyDuckParser.ProgramaContext):
        self.table_manager.start_program()
        
        # variables globales
        if ctx.vars_():
            self.visit(ctx.vars_())
            
        # declaracines de funciones
        if ctx.funcs():
            for func in ctx.funcs():
                self.visit(func)
        
        # visitar el cuerpo principal: (inicio) → <CUERPO> → (fin)
        self.visit(ctx.cuerpo())
        
        return None

    # 2. Agregar variables al scope actual
    def visitDeclarar_variables(self, ctx:BabyDuckParser.Declarar_variablesContext):
        var_type = ctx.tipo().getText()
        
        # iterar sobre todos los IDs declarados
        id_list_ctx = ctx.declarar_ids()
        for id_terminal in id_list_ctx.ID():
            var_name = id_terminal.getText()
            
            # validar que no sea una variable duplicada
            success = self.table_manager.declare_variable(var_name, var_type)
            
            if not success:
                raise BabyDuckError("semantico", f"Variable {var_name} ya fue declarada en este scope")

        return None

    # 3. Declarar una función en <FUNCS>
    def visitFuncs(self, ctx:BabyDuckParser.FuncsContext):
        """
        Crea el scope de la función, lo agrega al directorio y cambia al nuevo scope
        """

        func_name = ctx.ID().getText()
        return_type = "nula"
        if ctx.tipo():
            return_type = ctx.tipo().getText()
        
        # validar que la función no esté duplicada
        success = self.table_manager.add_function(func_name, return_type)
        if not success:
            raise BabyDuckError("semantico", f"La función {func_name} ya fue declarada")
            
        # puntero a la FuncInfo actual para los parámetros
        self.current_func_info = self.table_manager.lookup_function(func_name)
        
        if ctx.parametros():
            self.visit(ctx.parametros())
            
        if ctx.vars_():
            self.visit(ctx.vars_())
            
        self.visit(ctx.cuerpo())
        
        # restaurar al global, limpiar el puntero
        self.table_manager.end_function()
        self.current_func_info = None
        return None

    # 4. Visitar la regla <PARAMETROS> parte de <FUNCS>
    def visitParametros(self, ctx:BabyDuckParser.ParametrosContext):
        """
        Agrega parámetros a la lista de la función y a su tabla de variables.
        """
        if not self.current_func_info:
            raise BabyDuckError("semantico", "Error en directorio de funciones: no se encontró 'current_func_info' al visitar parámetros")
        
        for i in range(len(ctx.ID())):
            param_name = ctx.ID(i).getText()
            param_type = ctx.tipo(i).getText()
            
            self.current_func_info.add_param(param_type)
            
            # declarar como variable en el scope local
            success = self.table_manager.declare_variable(param_name, param_type)
            if not success:
                raise BabyDuckError("semantico", f"Parámetro {param_name} ya está declarado en el scope actual")

        return None