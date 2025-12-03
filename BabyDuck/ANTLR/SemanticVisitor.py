from BabuDuckError import BabyDuckError
from BabyDuckParser import BabyDuckParser
from BabyDuckVisitor import BabyDuckVisitor

from MemoryManager import MemoryManager
from semantic_cube import semantic_cube

class SemanticVisitor(BabyDuckVisitor):
    def __init__(self):
        # --- ESTRUCTURAS DE DATOS ---
        self.quadruples = []        
        self.operand_stack = [] 
        self.type_stack = []    
        self.operator_stack = []
        self.jump_stack = []
        
        self.cube = semantic_cube     
        self.mem_manager = MemoryManager()
        self.constant_table = {}
        
        # --- DIRECTORIO DE FUNCIONES ---
        self.dir_func = {
            "global": {
                "type": "void",      
                "start_quad": 0,     
                "vars_table": {},  
                "param_signature": [],
                "resources": {}     
            }
        }
        
        self.current_scope = "global"
        self.current_func_type = "void" # Auxiliar para validar retornos
        self.has_return_flag = False    # PN 4

    # ==========================================
    #       HELPERS
    # ==========================================

    def _get_op_string(self, token_type):
        op_map = {
            BabyDuckParser.MAS: "+", BabyDuckParser.MENOS: "-",
            BabyDuckParser.MULTIPLICACION: "*", BabyDuckParser.DIVISION: "/",
            BabyDuckParser.MAYOR_QUE: ">", BabyDuckParser.MENOR_QUE: "<",
            BabyDuckParser.DIFERENTE_DE: "!=", BabyDuckParser.IGUAL_QUE: "==",
            BabyDuckParser.ASIGNACION: "="
        }
        return op_map.get(token_type)

    def _generate_quad(self, op, left, right, res):
        self.quadruples.append((op, left, right, res))

    def _get_constant_addr(self, val_str, var_type):
        # Conversión de tipo
        val = int(val_str) if var_type == "entero" else float(val_str) if var_type == "flotante" else val_str
        
        # Búsqueda inversa para reutilizar constantes
        for addr, existing_val in self.constant_table.items():
            if existing_val == val:
                # Verificar rango para distinguir 10 (int) de 10.0 (float) si fuera necesario
                return addr

        # Crear nueva
        map_type = "int" if var_type == "entero" else "float" if var_type == "flotante" else "string"
        v_addr = self.mem_manager.get_virtual_address("const", map_type)
        self.constant_table[v_addr] = val
        return v_addr

    def _process_arithmetic_quad(self):
        # PN 11: Generación de cuádruplos aritméticos
        if not self.operator_stack: return

        right_op = self.operand_stack.pop()
        right_type = self.type_stack.pop()
        
        left_op = self.operand_stack.pop()
        left_type = self.type_stack.pop()
        
        operator = self.operator_stack.pop()
        
        res_type = self.cube.get(left_type, {}).get(right_type, {}).get(operator)
        
        if res_type == "error" or not res_type:
            raise BabyDuckError("semantico", f"Operacion invalida: {left_type} {operator} {right_type}")

        # Solicitar temporal
        # Mapeo de tipos para MemoryManager
        mem_type = "int" if res_type == "entero" else "float" if res_type == "flotante" else "bool"
        temp_addr = self.mem_manager.get_virtual_address("temp", mem_type)
        
        self._generate_quad(operator, left_op, right_op, temp_addr)
        self.operand_stack.append(temp_addr)
        self.type_stack.append(res_type)

    # ==========================================
    #       I. DEFINICIÓN Y ESTRUCTURA
    # ==========================================

    def visitPrograma(self, ctx: BabyDuckParser.ProgramaContext):
        # PN 1: Inicio del programa
        # El scope global ya está inicializado en __init__
        
        # Generar GOTO pendiente a main
        self._generate_quad("GOTO", None, None, "PENDING_MAIN")
        jump_main_index = len(self.quadruples) - 1

        # Visitar Variables Globales
        if ctx.vars_():
            self.visit(ctx.vars_())

        # Visitar Funciones
        # 'funcs' tiene cuantificador *, iteramos sobre la lista
        for func in ctx.funcs():
            self.visit(func)

        # PN 2: Token INICIO encontrado (Main)
        # Rellenar el salto a main
        self.quadruples[jump_main_index] = ("GOTO", None, None, len(self.quadruples))
        
        # Validar que no haya declaraciones en main (Gramática lo impide estructuralmente en 'cuerpo', ok)
        
        # Visitar Cuerpo Main
        self.visit(ctx.cuerpo())
        
        self._generate_quad("END", None, None, None)
        return None

    def visitVars(self, ctx: BabyDuckParser.VarsContext):
        # vars: VARS declarar_variables+
        for decl in ctx.declarar_variables():
            self.visit(decl)
        return None

    def visitDeclarar_variables(self, ctx: BabyDuckParser.Declarar_variablesContext):
        # PN 3: Declaración de variables
        # Obtener tipo
        var_type = ctx.tipo().getText() # "entero" o "flotante"
        mem_type = "int" if var_type == "entero" else "float"

        # Iterar sobre IDs en declarar_ids
        ids_ctx = ctx.declarar_ids()
        for token_id in ids_ctx.ID():
            var_name = token_id.getText()
            current_vars = self.dir_func[self.current_scope]["vars_table"]

            if var_name in current_vars:
                raise BabyDuckError("semantico", f"Variable re-declarada: {var_name}")
            
            # Asignar dirección
            scope_key = "global" if self.current_scope == "global" else "local"
            v_addr = self.mem_manager.get_virtual_address(scope_key, mem_type)
            
            # Agregar a tabla
            current_vars[var_name] = {
                "type": var_type,
                "direccion_virtual": v_addr
            }
        return None

    def visitFuncs(self, ctx: BabyDuckParser.FuncsContext):
        # PN 4: Flag return false
        self.has_return_flag = False
        
        # Obtener datos de firma
        func_type = ctx.tipo().getText() if ctx.tipo() else "void"
        self.current_func_type = func_type
        func_name = ctx.ID().getText()

        # PN 5: Validación y Creación de Función
        if func_name in self.dir_func:
            raise BabyDuckError("semantico", f"Funcion duplicada: {func_name}")

        self.dir_func[func_name] = {
            "type": func_type,
            "start_quad": len(self.quadruples),
            "vars_table": {},
            "param_signature": [],
            "resources": {}
        }
        
        # Si la función tiene retorno, asignar una dirección global para el valor de retorno
        if func_type != "void":
            mem_type = "int" if func_type == "entero" else "float"
            ret_addr = self.mem_manager.get_virtual_address("global", mem_type)
            self.dir_func[func_name]["return_addr"] = ret_addr

        # Resetear memoria y cambiar scope
        self.mem_manager.reset_local_memory()
        self.current_scope = func_name

        # PN 6: Parámetros
        if ctx.parametros():
            # Iterar parámetros manualmente (ID : tipo)
            params_node = ctx.parametros()
            ids = params_node.ID()
            types = params_node.tipo()
            
            for i in range(len(ids)):
                p_name = ids[i].getText()
                p_type = types[i].getText()
                p_mem_type = "int" if p_type == "entero" else "float"

                # Agregar a tabla de variables locales
                if p_name in self.dir_func[self.current_scope]["vars_table"]:
                    raise BabyDuckError("semantico", f"Parametro duplicado: {p_name}")
                
                v_addr = self.mem_manager.get_virtual_address("local", p_mem_type)
                
                self.dir_func[self.current_scope]["vars_table"][p_name] = {
                    "type": p_type,
                    "direccion_virtual": v_addr
                }
                
                # Agregar a firma
                self.dir_func[self.current_scope]["param_signature"].append(p_type)

        # Visitar variables locales si existen
        if ctx.vars_():
            self.visit(ctx.vars_())

        # Visitar cuerpo
        self.visit(ctx.cuerpo())

        # PN 8: Finalizar Función
        # Validar return obligatorio
        if self.current_func_type != "void" and not self.has_return_flag:
            raise BabyDuckError("semantico", f"Funcion {func_name} no retorno valor")

        # Generar RETURN void (por seguridad al final) y ENDFUNCTION
        self._generate_quad("RETURN", None, None, None)
        self._generate_quad("ENDFUNCTION", None, None, None)

        # Guardar recursos y limpiar
        # Calculamos recursos usados restando el actual menos el inicio del rango
        used_resources = {
            "local_entero": self.mem_manager.counters['local_entero'] - 3000,
            "local_flotante": self.mem_manager.counters['local_flotante'] - 4000,
            "temp_entero": self.mem_manager.counters['temp_entero'] - 5000,
            "temp_flotante": self.mem_manager.counters['temp_flotante'] - 6000,
            "temp_booleano": self.mem_manager.counters['temp_booleano'] - 7000
        }
        self.dir_func[self.current_scope]["resources"] = used_resources
        
        # Borrar vars_table local para ahorrar memoria (opcional, pero pedido en PN)
        # self.dir_func[self.current_scope]["vars_table"] = {} 
        
        self.current_scope = "global"
        self.current_func_type = "void"
        return None

    def visitDevuelve(self, ctx: BabyDuckParser.DevuelveContext):
        # PN 7: Token devolver
        if self.current_scope == "global":
            raise BabyDuckError("semantico", "No se puede usar 'devolver' en global")

        has_exp = ctx.exp() is not None

        # Validación Void
        if self.current_func_type == "void":
            if has_exp:
                raise BabyDuckError("semantico", "Funcion void no puede devolver valor")
            self._generate_quad("RETURN", None, None, None)
        
        # Validación con Tipo
        else:
            if not has_exp:
                raise BabyDuckError("semantico", "Funcion debe devolver un valor")
            
            # Evaluar expresión
            self.visit(ctx.exp()) # Esto pushea a operand_stack
            
            actual_type = self.type_stack.pop()
            actual_op = self.operand_stack.pop()

            if actual_type != self.current_func_type:
                raise BabyDuckError("semantico", f"Tipo de retorno incorrecto. Esperaba {self.current_func_type}, obtuvo {actual_type}")

            # Generar RETURN con valor -> DirGlobal de la función
            ret_dest = self.dir_func[self.current_scope]["return_addr"]
            self._generate_quad("RETURN", actual_op, None, ret_dest)

        self.has_return_flag = True
        return None

    # ==========================================
    #       II. EXPRESIONES
    # ==========================================

    def visitExpresion(self, ctx: BabyDuckParser.ExpresionContext):
        # expresion: exp ((RELACIONALES) exp)?
        self.visit(ctx.exp(0))

        if ctx.getChildCount() > 1:
            # Hay operador relacional
            op_token = ctx.getChild(1).getSymbol().type
            op_str = self._get_op_string(op_token)
            self.operator_stack.append(op_str) # PN 10
            
            self.visit(ctx.exp(1))
            self._process_arithmetic_quad() # PN 11

        return None

    def visitExp(self, ctx: BabyDuckParser.ExpContext):
        # exp: termino ((MAS|MENOS) termino)*
        self.visit(ctx.termino(0))

        for i in range(1, len(ctx.termino())):
            op_token = ctx.getChild(2*i - 1).getSymbol().type # Indice impar es el operador
            op_str = self._get_op_string(op_token)
            self.operator_stack.append(op_str) # PN 10
            
            self.visit(ctx.termino(i))
            
            # PN 11: Verificar jerarquía + -
            if self.operator_stack and self.operator_stack[-1] in ["+", "-"]:
                self._process_arithmetic_quad()
        return None

    def visitTermino(self, ctx: BabyDuckParser.TerminoContext):
        # termino: factor ((MULT|DIV) factor)*
        self.visit(ctx.factor(0))

        for i in range(1, len(ctx.factor())):
            op_token = ctx.getChild(2*i - 1).getSymbol().type
            op_str = self._get_op_string(op_token)
            self.operator_stack.append(op_str) # PN 10
            
            self.visit(ctx.factor(i))
            
            # PN 11: Verificar jerarquía * /
            if self.operator_stack and self.operator_stack[-1] in ["*", "/"]:
                self._process_arithmetic_quad()
        return None

    def visitFactor(self, ctx: BabyDuckParser.FactorContext):
        # factor: PARENTESIS_IZQUIERDO expresion PARENTESIS_DERECHO | (MAS | MENOS)? dato_o_llamada
        
        if ctx.PARENTESIS_IZQUIERDO():
            self.operator_stack.append("(") # Fondo falso
            self.visit(ctx.expresion())
            self.operator_stack.pop() # Sacar fondo falso
        else:
            # Manejo de signo unario
            sign = None
            if ctx.MAS(): sign = "+"
            if ctx.MENOS(): sign = "-"

            self.visit(ctx.dato_o_llamada())

            if sign:
                # Generar cuádruplo unario
                op_val = self.operand_stack.pop()
                op_type = self.type_stack.pop()
                
                # Validar tipo (solo numeros)
                if op_type not in ["entero", "flotante"]:
                    raise BabyDuckError("semantico", "Operador unario solo aplica a numeros")

                # Temp para resultado
                mem_type = "int" if op_type == "entero" else "float"
                res_addr = self.mem_manager.get_virtual_address("temp", mem_type)
                
                op_code = "unario+" if sign == "+" else "unario-"
                self._generate_quad(op_code, op_val, None, res_addr)
                
                self.operand_stack.append(res_addr)
                self.type_stack.append(op_type)
        return None

    def visitDato_o_llamada(self, ctx: BabyDuckParser.Dato_o_llamadaContext):
        # PN 9: ID o Cte
        
        # Caso 1: Constante (cte)
        if ctx.cte():
            self.visit(ctx.cte()) # Delega a visitCte
            return None

        # Caso 2: ID (Variable) o ID(...) (Llamada con retorno)
        var_name = ctx.ID().getText()
        
        # Ver si es llamada (tiene parentesis)
        if ctx.PARENTESIS_IZQUIERDO():
            # ES LLAMADA A FUNCIÓN (Dentro de expresión -> debe retornar valor)
            self._handle_function_call(ctx, must_return=True)
        else:
            # ES VARIABLE
            # Buscar en local, luego global
            vars_local = self.dir_func[self.current_scope]["vars_table"]
            vars_global = self.dir_func["global"]["vars_table"]
            
            info = vars_local.get(var_name) or vars_global.get(var_name)
            
            if not info:
                raise BabyDuckError("semantico", f"Variable no declarada: {var_name}")
            
            # Nota: Inicialización se valida en runtime (VM), aquí solo existencia.
            
            self.operand_stack.append(info["direccion_virtual"])
            self.type_stack.append(info["type"])
        
        return None

    def visitCte(self, ctx: BabyDuckParser.CteContext):
        # PN 9: Constantes
        if ctx.CTE_ENT():
            val = ctx.CTE_ENT().getText()
            addr = self._get_constant_addr(val, "entero")
            self.operand_stack.append(addr)
            self.type_stack.append("entero")
        elif ctx.CTE_FLOT():
            val = ctx.CTE_FLOT().getText()
            addr = self._get_constant_addr(val, "flotante")
            self.operand_stack.append(addr)
            self.type_stack.append("flotante")
        return None

    # ==========================================
    #       III. ESTATUTOS
    # ==========================================

    def visitContinuacion_de_estatuto_id(self, ctx: BabyDuckParser.Continuacion_de_estatuto_idContext):
        # Viene de estatuto: ID continuacion...
        # Puede ser Asignacion (= expr) o Llamada Void (( args ))
        
        # Necesitamos el ID previo. Como visitChildren no pasa contexto hacia arriba facil,
        # asumimos que el padre (visitEstatuto) manejó la lógica o el ID ya fue leído?
        # NO. ANTLR visita estatuto, lee ID, luego visita continuacion.
        # El ID NO ESTÁ en el contexto de continuacion. 
        # Solución: Acceder al padre desde ctx.
        
        parent = ctx.parentCtx
        if not isinstance(parent, BabyDuckParser.EstatutoContext):
             # Caso borde si la gramatica cambia, pero aqui es seguro
             return
             
        id_name = parent.ID().getText()

        if ctx.ASIGNACION():
            # PN 12: Asignación
            # Resolver expresión
            self.visit(ctx.expresion())
            
            res_val = self.operand_stack.pop()
            res_type = self.type_stack.pop()
            
            # Buscar ID destino
            vars_local = self.dir_func[self.current_scope]["vars_table"]
            vars_global = self.dir_func["global"]["vars_table"]
            
            target_info = vars_local.get(id_name) or vars_global.get(id_name)
            
            if not target_info:
                raise BabyDuckError("semantico", f"Variable no declarada: {id_name}")
                
            target_addr = target_info["direccion_virtual"]
            target_type = target_info["type"]
            
            # Validar compatibilidad (Cubo semantico para =)
            assign_res = self.cube.get(target_type, {}).get(res_type, {}).get("=")
            
            if assign_res == "error" or not assign_res:
                 raise BabyDuckError("semantico", f"Tipos incompatibles en asignacion: {target_type} = {res_type}")
            
            self._generate_quad("=", res_val, None, target_addr)
            
        elif ctx.PARENTESIS_IZQUIERDO():
            # Llamada a función VOID (estatuto solo)
            # Reconstruimos el nodo Dato_o_llamada logicamente o llamamos helper
            # Como la estructura de contextos es diferente, llamamos helper pasando "id_name" y los argumentos
            
            # PN 20, 21, 22 lógica manual para este caso
            if id_name not in self.dir_func:
                raise BabyDuckError("semantico", f"Funcion no declarada: {id_name}")
                
            self._generate_quad("ERA", id_name, None, None)
            
            # Procesar argumentos
            param_sig = self.dir_func[id_name]["param_signature"]
            args_ctx = ctx.expresion() # lista de expresiones
            
            if len(args_ctx) != len(param_sig):
                raise BabyDuckError("semantico", f"Numero de argumentos incorrecto. Esperaba {len(param_sig)}")
            
            for i, exp_ctx in enumerate(args_ctx):
                self.visit(exp_ctx)
                arg_val = self.operand_stack.pop()
                arg_type = self.type_stack.pop()
                
                expected_type = param_sig[i]
                if arg_type != expected_type:
                    raise BabyDuckError("semantico", f"Tipo de argumento {i+1} incorrecto. Esperaba {expected_type}")
                
                # Generar PARAM (DirArg, None, NumParam)
                # El NumParam es relativo a la nueva memoria. 
                # Necesitamos la direccion destino del parametro. 
                # Pero en diseño clásico PARAMETER solo toma NumParam o DirDestino.
                # VM implementation shows: PARAMETER left(val) res(target_addr).
                # Necesitamos saber la direccion virtual del parametro K en la funcion destino.
                # Hack: Iterar la vars_table de la funcion destino buscando los parametros en orden?
                # O confiar en que Param Signature tiene orden, y vars_table tambien?
                # Mejor: La VM usa 'mem_pending.set(res, val)'. 'res' debe ser la direccion LOCAL del parametro.
                
                # Obtener la direccion del parametro i en la funcion destino
                # Para esto requerimos recorrer la vars_table de esa funcion y encontrar el i-esimo parametro.
                # Como dir_func no guarda orden en vars_table (es dict), esto es peligroso.
                # CORRECCIÓN: Agregar direcciones de parametros ordenadas en dir_func al declarar.
                # Como no puedo cambiar dir_func struct ahora, asumimos que PARAMETER recibe:
                # PARAMETER, ValorOrigen, None, DireccionDestino
                
                # Buscamos nombre del parametro i en la funcion destino (complejo sin lista ordenada de nombres)
                # Solución robusta: Recalcular la direccion base de parametros.
                # Int parametros empiezan en 3000, Float en 4000. 
                # Pero no sabemos cuantos de cada uno van antes.
                # ASUMIRÉ: Debo buscar el nombre del parametro en la tabla de la funcion.
                # El visitor DEBE guardar orden de nombres de parametros.
                # Como no lo tengo, tendré que iterar values() y filtrar... ojalá coincida orden inserción (Python 3.7+ sí).
                
                target_func_vars = self.dir_func[id_name]["vars_table"]
                # Esto es lento pero seguro para encontrar la direccion del parametro i
                # Asumimos que los primeros N elementos de vars_table son los parametros.
                # Esto depende de visitFuncs (PN 6 inserta parametros primero).
                param_target_addr = list(target_func_vars.values())[i]["direccion_virtual"]
                
                self._generate_quad("PARAMETER", arg_val, None, param_target_addr)
                
            # PN 22: GOSUB
            start_addr = self.dir_func[id_name]["start_quad"]
            self._generate_quad("GOSUB", id_name, None, start_addr)
            
            # Si tuviera retorno, se ignoraría en un estatuto void, no generamos asignación temporal
        return None

    def visitImprime(self, ctx: BabyDuckParser.ImprimeContext):
        # PN 13: Imprime
        elements_node = ctx.imprimir_elementos()
        
        # Iterar hijos (pueden ser expresion o LETRERO)
        children = elements_node.children
        for child in children:
            if child.getSymbol().type == BabyDuckParser.COMA:
                continue
                
            if isinstance(child, BabyDuckParser.ExpresionContext):
                self.visit(child)
                val = self.operand_stack.pop()
                self.type_stack.pop()
                self._generate_quad("PRINT", None, None, val)
                
            elif child.getSymbol().type == BabyDuckParser.LETRERO:
                raw_str = child.getText()
                clean_str = raw_str[1:-1] # Quitar comillas
                
                # Checar constantes strings
                s_addr = self._get_constant_addr(clean_str, "string")
                self._generate_quad("PRINT", None, None, s_addr)
        return None

    # ==========================================
    #       IV. CONTROL DE FLUJO
    # ==========================================

    def visitCondicion(self, ctx: BabyDuckParser.CondicionContext):
        # PN 14: IF
        self.visit(ctx.expresion())
        
        cond_type = self.type_stack.pop()
        cond_val = self.operand_stack.pop()
        
        if cond_type != "booleano":
            raise BabyDuckError("semantico", "Expresion de condicion debe ser booleana")
            
        self._generate_quad("GOTOF", cond_val, None, "PENDING_GOTOF")
        self.jump_stack.append(len(self.quadruples) - 1)
        
        # Cuerpo IF
        self.visit(ctx.cuerpo(0)) # Primer cuerpo
        
        # PN 15: ELSE (SINO)
        if ctx.SINO():
            self._generate_quad("GOTO", None, None, "PENDING_GOTO")
            goto_index = len(self.quadruples) - 1
            
            # Rellenar GOTOF
            gotof_index = self.jump_stack.pop()
            self.quadruples[gotof_index] = ("GOTOF", self.quadruples[gotof_index][1], None, len(self.quadruples))
            
            self.jump_stack.append(goto_index)
            
            # Cuerpo ELSE
            self.visit(ctx.cuerpo(1))
            
        # PN 16: Fin IF
        end_jump_index = self.jump_stack.pop()
        # Rellenar GOTO (del else) o GOTOF (si no hubo else)
        op, arg1, _, _ = self.quadruples[end_jump_index]
        self.quadruples[end_jump_index] = (op, arg1, None, len(self.quadruples))
        
        return None

    def visitCiclo(self, ctx: BabyDuckParser.CicloContext):
        # PN 17: While Start
        start_index = len(self.quadruples)
        self.jump_stack.append(start_index)
        
        # Expresion
        self.visit(ctx.expresion())
        
        # PN 18: Evaluar bool
        cond_type = self.type_stack.pop()
        cond_val = self.operand_stack.pop()
        
        if cond_type != "booleano":
            raise BabyDuckError("semantico", "Expresion de ciclo debe ser booleana")
            
        self._generate_quad("GOTOF", cond_val, None, "PENDING_GOTOF")
        self.jump_stack.append(len(self.quadruples) - 1)
        
        # Cuerpo
        self.visit(ctx.cuerpo())
        
        # PN 19: Fin While
        gotof_index = self.jump_stack.pop()
        return_index = self.jump_stack.pop()
        
        self._generate_quad("GOTO", None, None, return_index)
        
        # Rellenar GOTOF
        op, arg1, _, _ = self.quadruples[gotof_index]
        self.quadruples[gotof_index] = (op, arg1, None, len(self.quadruples))
        
        return None

    # ==========================================
    #       V. LLAMADAS A FUNCIÓN
    # ==========================================

    def _handle_function_call(self, ctx, must_return):
        # Helper para llamadas (PN 20, 21, 22)
        func_name = ctx.ID().getText()
        
        # PN 20
        if func_name not in self.dir_func:
            raise BabyDuckError("semantico", f"Funcion no declarada: {func_name}")
            
        self._generate_quad("ERA", func_name, None, None)
        
        # PN 21: Argumentos
        param_sig = self.dir_func[func_name]["param_signature"]
        
        # ctx puede ser Dato_o_llamada (tiene expresion()) o Continuacion (tiene expresion())
        # Ambos retornan lista de expresiones
        args_ctx = ctx.expresion() 
        
        if len(args_ctx) != len(param_sig):
            raise BabyDuckError("semantico", f"Numero de argumentos incorrecto en {func_name}")
        
        target_func_vars = self.dir_func[func_name]["vars_table"]
        param_list_addrs = [v["direccion_virtual"] for v in target_func_vars.values()] # Asumiendo orden insercion
        
        for i, exp_ctx in enumerate(args_ctx):
            self.visit(exp_ctx)
            arg_val = self.operand_stack.pop()
            arg_type = self.type_stack.pop()
            
            if arg_type != param_sig[i]:
                raise BabyDuckError("semantico", f"Tipo de argumento {i+1} incorrecto en {func_name}")
            
            # Dirección destino del parametro
            param_dest = param_list_addrs[i]
            self._generate_quad("PARAMETER", arg_val, None, param_dest)
            
        # PN 22: GOSUB y Retorno
        start_addr = self.dir_func[func_name]["start_quad"]
        self._generate_quad("GOSUB", func_name, None, start_addr)
        
        return_type = self.dir_func[func_name]["type"]
        
        if must_return:
            if return_type == "void":
                raise BabyDuckError("semantico", f"Funcion void {func_name} no puede usarse en expresion")
            
            # Asignar resultado global a temporal local
            ret_global_addr = self.dir_func[func_name]["return_addr"]
            
            mem_type = "int" if return_type == "entero" else "float"
            temp_addr = self.mem_manager.get_virtual_address("temp", mem_type)
            
            self._generate_quad("=", ret_global_addr, None, temp_addr)
            self.operand_stack.append(temp_addr)
            self.type_stack.append(return_type)