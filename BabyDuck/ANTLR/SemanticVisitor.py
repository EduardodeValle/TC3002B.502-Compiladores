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

    # 1. Inicializar el scope global en <PROGRAMA>
    def visit_programa(self, ctx:BabyDuckParser.ProgramaContext):
        self.table_manager.start_program()
        
        # visitar variables globales
        if ctx.vars_():
            self.visit(ctx.vars_())
            
        # visitar declaracoines de funciones
        if ctx.funcs():
            for func in ctx.funcs():
                self.visit(func)
        
        # visitar el cuerpo principal: (inicio) → <CUERPO> → (fin)
        self.visit(ctx.cuerpo())
        
        return None