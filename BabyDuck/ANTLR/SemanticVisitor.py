from BabyDuckError import BabyDuckError
from BabyDuckParser import BabyDuckParser
from BabyDuckVisitor import BabyDuckVisitor

from MemoryManager import MemoryManager
from semantic_cube import semantic_cube

class SemanticVisitor(BabyDuckVisitor):
    def __init__(self):
        # --- ESTRUCTURAS DE DATOS (PILAS Y LISTAS) ---
        self.quadruples = []
        self.operand_stack = []
        self.type_stack = []
        self.operator_stack = []
        self.jump_stack = []
        self.pending_jump = None

        self.cube = semantic_cube
        self.mem_manager = MemoryManager()
        self.constant_table = {}  # {(valor, tipo): {value, type, direccion_virtual}}

        # --- DIRECTORIO DE FUNCIONES (TABLA DE SÍMBOLOS) ---
        # Inicializamos con el scope 'global' ya listo
        self.dir_func = {
            "global": {
                "type": "void",
                "start_quad": 0,
                "vars_table": {},
                "param_signature": [],  # Lista de tipos en orden
                "param_addresses": [],  # Lista de direcciones en orden (para PARAMETER)
                "resources": {}
            }
        }

        self.current_scope = "global"
        self.current_id = None
        self.current_function_has_return = False

    # helper functions para el directorio de funciones y tabla de simbolos

    def _create_function_entry(self, return_type, start_quad):
        """
        Crea el template vacío para una nueva función.
        """
        return {
            "type": return_type,
            "start_quad": start_quad,
            "vars_table": {},
            "param_signature": [],  # Lista ordenada de tipos de parámetros (ej: ['entero', 'flotante'])
            "param_addresses": [],  # Lista ordenada de direcciones de parámetros (para PARAMETER)
            "resources": {          # Cantidad de recursos que necesitará la VM
                "local_entero": 0,
                "local_flotante": 0,
                "temp_entero": 0,
                "temp_flotante": 0,
                "temp_booleano": 0
            }
        }

    def _declare_function(self, func_name, return_type, start_quad):
        """
        Registra una nueva función y cambia el scope actual.
        """
        if func_name in self.dir_func:
            raise BabyDuckError("semantico", f"La funcion '{func_name}' ya existe")
            
        # 1. Crear entrada
        self.dir_func[func_name] = self._create_function_entry(return_type, start_quad)
        
        # 2. Cambiar el puntero de scope
        self.current_scope = func_name
        
        # 3. Reiniciar contadores de memoria local y temporal (IMPORTANTE)
        self.mem_manager.reset_local_memory()

    def _end_function_logic(self):
        """
        Se llama cuando se termina de procesar una función.
        Calcula los recursos usados basándose en los contadores del MemoryManager.
        """
        # Obtenemos los contadores actuales del MemoryManager
        # Supongamos que tu MemoryManager tiene un método para ver el estado actual o accedes a counters
        # Restamos el limite inferior para saber cuantos usamos (ej: si counter va en 3005 y base es 3000, usamos 5)
        
        used_resources = {
            "local_entero": self.mem_manager.counters['local_entero'] - self.mem_manager.memory_map['local_entero']['start'],
            "local_flotante": self.mem_manager.counters['local_flotante'] - self.mem_manager.memory_map['local_flotante']['start'],
            "temp_entero": self.mem_manager.counters['temp_entero'] - self.mem_manager.memory_map['temp_entero']['start'],
            "temp_flotante": self.mem_manager.counters['temp_flotante'] - self.mem_manager.memory_map['temp_flotante']['start'],
            "temp_booleano": self.mem_manager.counters['temp_booleano'] - self.mem_manager.memory_map['temp_booleano']['start'],
        }

        # Guardamos esto en el DirFunc de la función actual
        self.dir_func[self.current_scope]["resources"] = used_resources
        
        # Insertar cuádruplo ENDFUNC
        self.quadruples.append(("ENDFUNCTION", None, None, None))
        
        # Limpiar tabla de temporales si usas una aparte, y regresar scope a global si es necesario
        # (Aunque típicamente en ANTLR simplemente sales del nodo y el scope cambia cuando entras a otra func)
        self.current_scope = "global"

    def _create_var_entry(self, var_type, virtual_address, initialized=False):
        """
        Crea el template para una variable (sea local o global).
        """
        return {
            "type": var_type,
            "direccion_virtual": virtual_address,
            "initialized": initialized
        }

    def _declare_variable(self, var_name, var_type, is_param=False):
        """
        Registra una variable en el scope actual (Global o Función).
        Los parámetros se marcan como inicializados automáticamente.
        """
        current_vars = self.dir_func[self.current_scope]["vars_table"]

        if var_name in current_vars:
            raise BabyDuckError("semantico", f"La variable '{var_name}' ya fue declarada en el scope '{self.current_scope}'.")

        # 1. Pedir dirección virtual al MemoryManager
        scope_type = "global" if self.current_scope == "global" else "local"
        virtual_addr = self.mem_manager.get_virtual_address(scope_type, var_type)

        # 2. Guardar en la tabla (parámetros ya están inicializados)
        current_vars[var_name] = self._create_var_entry(var_type, virtual_addr, initialized=is_param)

        return virtual_addr  # Retornar la dirección asignada

    # Otros helper functions

    def _lookup_variable(self, var_name):
        """
        Busca una variable primero en el scope local, luego en el global.
        Retorna un diccionario con 'type', 'direccion_virtual', 'initialized', o None si no existe.
        """
        # Primero buscar en el scope actual
        current_vars = self.dir_func[self.current_scope]["vars_table"]
        if var_name in current_vars:
            return current_vars[var_name]

        # Si no está en local, buscar en global (solo si no estamos en global)
        if self.current_scope != "global":
            global_vars = self.dir_func["global"]["vars_table"]
            if var_name in global_vars:
                return global_vars[var_name]

        # No se encontró la variable
        return None

    def _mark_variable_initialized(self, var_name):
        """
        Marca una variable como inicializada en su tabla de símbolos.
        """
        current_vars = self.dir_func[self.current_scope]["vars_table"]
        if var_name in current_vars:
            current_vars[var_name]["initialized"] = True
        elif self.current_scope != "global":
            global_vars = self.dir_func["global"]["vars_table"]
            if var_name in global_vars:
                global_vars[var_name]["initialized"] = True

    def _add_constant(self, value, const_type):
        """
        Agrega una constante a la tabla de constantes y retorna su dirección virtual.
        Si la constante ya existe, retorna la dirección existente.
        """
        # Usar una tupla (valor, tipo) como clave para identificar la constante
        const_key = (value, const_type)

        if const_key in self.constant_table:
            return self.constant_table[const_key]["direccion_virtual"]

        # Obtener dirección virtual para la constante
        scope_type = "const"
        virtual_addr = self.mem_manager.get_virtual_address(scope_type, const_type)

        # Guardar en la tabla de constantes
        self.constant_table[const_key] = {
            "value": value,
            "type": const_type,
            "direccion_virtual": virtual_addr
        }

        return virtual_addr

    def _generate_quadruple(self, operator, left_operand, right_operand, result):
        """
        Helper para generar un cuádruplo y agregarlo a la lista.
        Retorna el índice del cuádruplo generado.
        """
        quad = (operator, left_operand, right_operand, result)
        self.quadruples.append(quad)
        return len(self.quadruples) - 1

    def _fill_quadruple(self, quad_index, result_value):
        """
        Rellena un cuádruplo pendiente con el valor de resultado.
        """
        operator, left, right, _ = self.quadruples[quad_index]
        self.quadruples[quad_index] = (operator, left, right, result_value)

    def _solve_pending_operations(self, allowed_operators):
        """
        Resuelve operaciones pendientes según precedencia.
        Genera cuádruplos para las operaciones válidas en operator_stack.
        """
        while (self.operator_stack and
               self.operator_stack[-1] != "(" and
               self.operator_stack[-1] in allowed_operators):

            # Pop operador y operandos
            operator = self.operator_stack.pop()
            right_operand = self.operand_stack.pop()
            right_type = self.type_stack.pop()
            left_operand = self.operand_stack.pop()
            left_type = self.type_stack.pop()

            # Validar con el cubo semántico
            try:
                result_type = self.cube[left_type][right_type][operator]
            except KeyError:
                raise BabyDuckError("semantico",
                    f"Operación inválida: {left_type} {operator} {right_type}")

            if result_type == "error":
                raise BabyDuckError("semantico",
                    f"Operación inválida: {left_type} {operator} {right_type}")

            # Generar temporal para el resultado
            temp_addr = self.mem_manager.get_virtual_address("temp", result_type)

            # Generar cuádruplo
            self._generate_quadruple(operator, left_operand, right_operand, temp_addr)

            # Push del resultado temporal a las pilas
            self.operand_stack.append(temp_addr)
            self.type_stack.append(result_type)

    def get_constants_for_vm(self):
        """
        Retorna un diccionario compatible con la VM: {dirección: valor}
        """
        constants_map = {}
        for const_info in self.constant_table.values():
            addr = const_info["direccion_virtual"]
            value = const_info["value"]
            constants_map[addr] = value
        return constants_map

    # ====================================================================
    # PUNTOS NEURÁLGICOS - VISITOR METHODS
    # ====================================================================

    # Punto Neurálgico 1-3: Visitar PROGRAMA
    def visitPrograma(self, ctx):
        """
        Puntos Neurálgicos 1-3:
        - Inicializar scope global y generar primer cuádruplo GOTO pendiente
        - Al encontrar 'inicio', rellenar el GOTO
        - Al encontrar 'fin', generar END
        """
        # Punto 1: Generar cuádruplo GOTO pendiente que saltará a main()
        self.pending_jump = self._generate_quadruple("GOTO", None, None, None)

        # Procesar vars globales si existen
        if ctx.vars_():
            self.visit(ctx.vars_())

        # Procesar funciones
        for func in ctx.funcs():
            self.visit(func)

        # Punto 2: Al encontrar 'inicio' (main)
        # Rellenar el GOTO pendiente con el cuádruplo actual
        self._fill_quadruple(self.pending_jump, len(self.quadruples))

        # Cambiar scope a global para main
        self.current_scope = "global"

        # Visitar el cuerpo de main
        self.visit(ctx.cuerpo())

        # Punto 3: Al encontrar 'fin'
        # Generar cuádruplo final END
        self._generate_quadruple("END", None, None, None)

        return None

    # Punto Neurálgico 4: Visitar VARS
    def visitVars(self, ctx):
        """
        Punto Neurálgico 4: Procesar declaraciones de variables
        """
        for declaracion in ctx.declarar_variables():
            self.visit(declaracion)
        return None

    def visitDeclarar_variables(self, ctx):
        """
        Visita cada declaración de variable y las registra
        """
        # Obtener el tipo de las variables
        tipo_ctx = ctx.tipo()
        var_type = self.visit(tipo_ctx)

        # Obtener los IDs de las variables
        ids_ctx = ctx.declarar_ids()
        var_names = self.visit(ids_ctx)

        # Declarar cada variable
        for var_name in var_names:
            self._declare_variable(var_name, var_type, is_param=False)

        return None

    def visitDeclarar_ids(self, ctx):
        """
        Retorna una lista con los nombres de las variables
        """
        var_names = []
        for id_token in ctx.ID():
            var_names.append(id_token.getText())
        return var_names

    def visitTipo(self, ctx):
        """
        Retorna el tipo de dato como string
        """
        if ctx.ENTERO():
            return "entero"
        elif ctx.FLOTANTE():
            return "flotante"
        return None

    # Puntos Neurálgicos 5-9: Visitar FUNCS
    def visitFuncs(self, ctx):
        """
        Puntos Neurálgicos 5-9: Procesamiento completo de funciones
        """
        if ctx.NULA():
            return_type = "void"
        else:
            return_type = self.visit(ctx.tipo())

        func_name = ctx.ID().getText()
        start_quad = len(self.quadruples)

        self._declare_function(func_name, return_type, start_quad)

        if return_type != "void":
            return_addr = self.mem_manager.get_virtual_address("global", return_type)
            self.dir_func[func_name]["vars_table"]["__return__"] = {
                "type": return_type,
                "direccion_virtual": return_addr,
                "initialized": True
            }

        if ctx.parametros():
            self.visit(ctx.parametros())

        if ctx.vars_():
            self.visit(ctx.vars_())

        self.current_function_has_return = False

        cuerpo_ctx = ctx.cuerpo()
        for estatuto in cuerpo_ctx.estatuto():
            self.visit(estatuto)

        if not self.current_function_has_return and return_type != "void":
            raise BabyDuckError("semantico",
                f"La función '{func_name}' debe tener al menos un 'devolver'")

        if return_type == "void" and not self.current_function_has_return:
            self._generate_quadruple("RETURN", None, None, None)

        self._end_function_logic()

        return None

    def visitParametros(self, ctx):
        """
        Punto 7: Procesar parámetros y marcarlos como variables locales
        """
        ids = ctx.ID()
        tipos = ctx.tipo()

        for i in range(len(ids)):
            param_name = ids[i].getText()
            param_type = self.visit(tipos[i])

            # Declarar como variable local (marcado como parámetro)
            param_addr = self._declare_variable(param_name, param_type, is_param=True)

            # Agregar a la firma de parámetros
            self.dir_func[self.current_scope]["param_signature"].append(param_type)
            # Agregar dirección a la lista de direcciones de parámetros
            self.dir_func[self.current_scope]["param_addresses"].append(param_addr)

        return None

    # Punto 8: Visitar DEVOLVER
    def visitDevuelve(self, ctx):
        """
        Punto Neurálgico 8: Procesar token 'devolver'
        """
        if self.current_scope == "global":
            raise BabyDuckError("semantico",
                "No se puede usar 'devolver' en el programa principal")

        self.current_function_has_return = True
        func_return_type = self.dir_func[self.current_scope]["type"]

        if func_return_type == "void":
            if ctx.exp():
                raise BabyDuckError("semantico",
                    "Función 'void' no puede devolver un valor")
            self._generate_quadruple("RETURN", None, None, None)
        else:
            if not ctx.exp():
                raise BabyDuckError("semantico",
                    f"Función de tipo '{func_return_type}' debe devolver un valor")

            self.visit(ctx.exp())

            expr_type = self.type_stack.pop()
            expr_addr = self.operand_stack.pop()

            if expr_type != func_return_type:
                raise BabyDuckError("semantico",
                    f"Tipo de retorno incorrecto. Se esperaba '{func_return_type}' pero se obtuvo '{expr_type}'")

            func_return_addr = self.dir_func[self.current_scope]["vars_table"]["__return__"]["direccion_virtual"]
            self._generate_quadruple("RETURN", expr_addr, None, func_return_addr)

        return None

    # Visitar CUERPO
    def visitCuerpo(self, ctx):
        """
        Visita el cuerpo de una función o bloque
        """
        for estatuto in ctx.estatuto():
            self.visit(estatuto)
        return None

    # Visitar ESTATUTO
    def visitEstatuto(self, ctx):
        """
        Delega al tipo de estatuto correcto
        """
        if ctx.continuacion_de_estatuto_id():
            # Es una asignación o llamada a función
            var_name = ctx.ID().getText()
            self.current_id = var_name  # Guardar para usar en continuación
            self.visit(ctx.continuacion_de_estatuto_id())
        elif ctx.condicion():
            self.visit(ctx.condicion())
        elif ctx.ciclo():
            self.visit(ctx.ciclo())
        elif ctx.imprime():
            self.visit(ctx.imprime())
        elif ctx.devuelve():
            self.visit(ctx.devuelve())
        else:
            # Bloque anidado con corchetes
            for estatuto in ctx.estatuto():
                self.visit(estatuto)
        return None

    def visitContinuacion_de_estatuto_id(self, ctx):
        """
        Procesa asignación o llamada a función después de un ID
        """
        if ctx.ASIGNACION():
            # Punto Neurálgico 12: Asignación
            var_name = self.current_id

            # Buscar la variable
            var_info = self._lookup_variable(var_name)
            if not var_info:
                raise BabyDuckError("semantico",
                    f"Variable '{var_name}' no declarada")

            # Evaluar la expresión del lado derecho
            self.visit(ctx.expresion(0))

            # Validar compatibilidad de tipos
            expr_type = self.type_stack.pop()
            expr_addr = self.operand_stack.pop()
            var_type = var_info["type"]

            # Consultar cubo semántico para asignación
            try:
                assignment_result = self.cube[var_type][expr_type]["="]
            except KeyError:
                assignment_result = "error"

            if assignment_result == "error":
                raise BabyDuckError("semantico",
                    f"No se puede asignar '{expr_type}' a variable de tipo '{var_type}'")

            # Generar cuádruplo de asignación
            var_addr = var_info["direccion_virtual"]
            self._generate_quadruple("=", expr_addr, None, var_addr)

            # Marcar variable como inicializada
            self._mark_variable_initialized(var_name)

        else:
            # Es una llamada a función
            # Puntos Neurálgicos 20-22: Llamada a función
            func_name = self.current_id

            # Validar que existe la función
            if func_name not in self.dir_func:
                raise BabyDuckError("semantico",
                    f"Función '{func_name}' no declarada")

            func_info = self.dir_func[func_name]

            # Generar ERA
            self._generate_quadruple("ERA", func_name, None, None)

            # Procesar argumentos
            param_count = 0
            expected_params = func_info["param_signature"]
            param_addresses = func_info["param_addresses"]

            if ctx.expresion():
                for expr_ctx in ctx.expresion():
                    # Evaluar expresión del argumento
                    self.visit(expr_ctx)

                    # Verificar tipo del parámetro
                    if param_count >= len(expected_params):
                        raise BabyDuckError("semantico",
                            f"Demasiados argumentos para función '{func_name}'")

                    arg_type = self.type_stack.pop()
                    arg_addr = self.operand_stack.pop()
                    expected_type = expected_params[param_count]

                    if arg_type != expected_type:
                        raise BabyDuckError("semantico",
                            f"Argumento {param_count + 1} de '{func_name}': se esperaba '{expected_type}' pero se obtuvo '{arg_type}'")

                    # Generar PARAMETER con dirección destino
                    param_dest_addr = param_addresses[param_count]
                    self._generate_quadruple("PARAMETER", arg_addr, None, param_dest_addr)
                    param_count += 1

            # Verificar cantidad de parámetros
            if param_count != len(expected_params):
                raise BabyDuckError("semantico",
                    f"Función '{func_name}' espera {len(expected_params)} argumentos pero se recibieron {param_count}")

            # Generar GOSUB
            start_addr = func_info["start_quad"]
            self._generate_quadruple("GOSUB", func_name, None, start_addr)

            # Si la función retorna un valor, guardarlo en temporal
            if func_info["type"] != "void":
                func_return_addr = func_info["vars_table"]["__return__"]["direccion_virtual"]
                temp_addr = self.mem_manager.get_virtual_address("temp", func_info["type"])
                self._generate_quadruple("=", func_return_addr, None, temp_addr)

                # Push del temporal a las pilas
                self.operand_stack.append(temp_addr)
                self.type_stack.append(func_info["type"])

        return None

    # Punto Neurálgico 13: Visitar IMPRIME
    def visitImprime(self, ctx):
        """
        Punto Neurálgico 13: Generar cuádruplos PRINT
        """
        self.visit(ctx.imprimir_elementos())
        return None

    def visitImprimir_elementos(self, ctx):
        """
        Procesa los elementos a imprimir
        """
        expresiones = ctx.expresion() if ctx.expresion() else []
        letreros = ctx.LETRERO() if ctx.LETRERO() else []

        expr_idx = 0
        letrero_idx = 0

        for child in ctx.children:
            if hasattr(child, 'getRuleIndex') and child.getRuleIndex() == BabyDuckParser.RULE_expresion:
                self.visit(expresiones[expr_idx])
                expr_addr = self.operand_stack.pop()
                self.type_stack.pop()
                self._generate_quadruple("PRINT", None, None, expr_addr)
                expr_idx += 1

            elif hasattr(child, 'getSymbol') and child.getSymbol().type == BabyDuckParser.LETRERO:
                string_value = letreros[letrero_idx].getText()
                string_value = string_value[1:-1]
                string_addr = self._add_constant(string_value, "string")
                self._generate_quadruple("PRINT", None, None, string_addr)
                letrero_idx += 1

        return None

    # Puntos Neurálgicos 14-16: Visitar CONDICION
    def visitCondicion(self, ctx):
        """
        Puntos Neurálgicos 14-16: Procesar if/else
        """
        # Punto 14: Evaluar expresión
        self.visit(ctx.expresion())

        # Validar que sea booleana
        expr_type = self.type_stack.pop()
        expr_addr = self.operand_stack.pop()

        if expr_type != "booleano":
            raise BabyDuckError("semantico",
                "La condición del 'si' debe ser una expresión booleana")

        # Generar GOTOF pendiente
        gotof_index = self._generate_quadruple("GOTOF", expr_addr, None, None)
        self.jump_stack.append(gotof_index)

        # Visitar cuerpo del if
        self.visit(ctx.cuerpo(0))

        # Punto 15: Si hay else
        if len(ctx.cuerpo()) > 1:
            # Generar GOTO pendiente
            goto_index = self._generate_quadruple("GOTO", None, None, None)

            # Rellenar GOTOF con posición actual
            gotof_idx = self.jump_stack.pop()
            self._fill_quadruple(gotof_idx, len(self.quadruples))

            # Visitar cuerpo del else
            self.visit(ctx.cuerpo(1))

            # Rellenar GOTO
            self._fill_quadruple(goto_index, len(self.quadruples))
        else:
            # Punto 16: Rellenar GOTOF
            gotof_idx = self.jump_stack.pop()
            self._fill_quadruple(gotof_idx, len(self.quadruples))

        return None

    # Puntos Neurálgicos 17-19: Visitar CICLO
    def visitCiclo(self, ctx):
        """
        Puntos Neurálgicos 17-19: Procesar while
        """
        # Punto 17: Push de posición antes de evaluar expresión
        start_expr_index = len(self.quadruples)
        self.jump_stack.append(start_expr_index)

        # Punto 18: Evaluar expresión
        self.visit(ctx.expresion())

        # Validar que sea booleana
        expr_type = self.type_stack.pop()
        expr_addr = self.operand_stack.pop()

        if expr_type != "booleano":
            raise BabyDuckError("semantico",
                "La condición del 'mientras' debe ser una expresión booleana")

        # Generar GOTOF pendiente
        gotof_index = self._generate_quadruple("GOTOF", expr_addr, None, None)
        self.jump_stack.append(gotof_index)

        # Visitar cuerpo del while
        self.visit(ctx.cuerpo())

        # Punto 19: Finalizar ciclo
        # Sacar índice de GOTOF
        gotof_idx = self.jump_stack.pop()
        # Sacar índice de inicio de expresión
        start_idx = self.jump_stack.pop()

        # Generar GOTO para re-evaluar expresión
        self._generate_quadruple("GOTO", None, None, start_idx)

        # Rellenar GOTOF para salir del while
        self._fill_quadruple(gotof_idx, len(self.quadruples))

        return None

    # Visitar EXPRESION
    def visitExpresion(self, ctx):
        """
        Procesa expresiones con operadores relacionales
        """
        # Visitar primer exp
        self.visit(ctx.exp(0))

        # Si hay operador relacional
        if len(ctx.exp()) > 1:
            # Obtener operador
            if ctx.MAYOR_QUE():
                operator = ">"
            elif ctx.MENOR_QUE():
                operator = "<"
            elif ctx.DIFERENTE_DE():
                operator = "!="
            elif ctx.IGUAL_QUE():
                operator = "=="

            # Push operador
            self.operator_stack.append(operator)

            # Visitar segundo exp
            self.visit(ctx.exp(1))

            # Resolver operación relacional
            self._solve_pending_operations([">", "<", "!=", "=="])

        return None

    def visitExp(self, ctx):
        """
        Procesa suma y resta
        """
        # Visitar primer término
        self.visit(ctx.termino(0))

        # Procesar operadores + y -
        for i in range(1, len(ctx.termino())):
            # Obtener operador
            if ctx.MAS(i-1):
                operator = "+"
            elif ctx.MENOS(i-1):
                operator = "-"

            # Push operador
            self.operator_stack.append(operator)

            # Visitar término
            self.visit(ctx.termino(i))

            # Resolver operaciones pendientes
            self._solve_pending_operations(["+", "-"])

        return None

    def visitTermino(self, ctx):
        """
        Procesa multiplicación y división
        """
        # Visitar primer factor
        self.visit(ctx.factor(0))

        # Procesar operadores * y /
        for i in range(1, len(ctx.factor())):
            # Obtener operador
            if ctx.MULTIPLICACION(i-1):
                operator = "*"
            elif ctx.DIVISION(i-1):
                operator = "/"

            # Push operador
            self.operator_stack.append(operator)

            # Visitar factor
            self.visit(ctx.factor(i))

            # Resolver operaciones pendientes
            self._solve_pending_operations(["*", "/"])

        return None

    def visitFactor(self, ctx):
        """
        Procesa factores con signos unarios y paréntesis
        """
        # Si hay paréntesis
        if ctx.PARENTESIS_IZQUIERDO():
            # Push de paréntesis falso
            self.operator_stack.append("(")

            # Visitar expresión
            self.visit(ctx.expresion())

            # Pop del paréntesis falso
            if self.operator_stack and self.operator_stack[-1] == "(":
                self.operator_stack.pop()

        # Si hay signo unario
        elif ctx.MAS() or ctx.MENOS():
            # Visitar dato o llamada
            self.visit(ctx.dato_o_llamada())

            # Si es unario negativo, generar cuádruplo
            if ctx.MENOS():
                operand = self.operand_stack.pop()
                operand_type = self.type_stack.pop()

                # Generar temporal para el resultado
                temp_addr = self.mem_manager.get_virtual_address("temp", operand_type)

                # Generar cuádruplo unario-
                self._generate_quadruple("unario-", operand, None, temp_addr)

                # Push del resultado
                self.operand_stack.append(temp_addr)
                self.type_stack.append(operand_type)
            # Si es unario positivo, no hacer nada (ya está en las pilas)

        else:
            # Sin paréntesis ni signo
            self.visit(ctx.dato_o_llamada())

        return None

    def visitDato_o_llamada(self, ctx):
        """
        Puntos Neurálgicos 9-11: Procesa ID, constantes o llamadas a función
        """
        if ctx.ID():
            var_name = ctx.ID().getText()

            # Verificar si es llamada a función
            if ctx.PARENTESIS_IZQUIERDO():
                # Es llamada a función
                func_name = var_name

                # Validar que existe la función
                if func_name not in self.dir_func:
                    raise BabyDuckError("semantico",
                        f"Función '{func_name}' no declarada")

                func_info = self.dir_func[func_name]

                # Generar ERA
                self._generate_quadruple("ERA", func_name, None, None)

                # Procesar argumentos
                param_count = 0
                expected_params = func_info["param_signature"]
                param_addresses = func_info["param_addresses"]

                if ctx.expresion():
                    for expr_ctx in ctx.expresion():
                        # Evaluar expresión del argumento
                        self.visit(expr_ctx)

                        # Verificar tipo del parámetro
                        if param_count >= len(expected_params):
                            raise BabyDuckError("semantico",
                                f"Demasiados argumentos para función '{func_name}'")

                        arg_type = self.type_stack.pop()
                        arg_addr = self.operand_stack.pop()
                        expected_type = expected_params[param_count]

                        if arg_type != expected_type:
                            raise BabyDuckError("semantico",
                                f"Argumento {param_count + 1} de '{func_name}': se esperaba '{expected_type}' pero se obtuvo '{arg_type}'")

                        # Generar PARAMETER con dirección destino
                        param_dest_addr = param_addresses[param_count]
                        self._generate_quadruple("PARAMETER", arg_addr, None, param_dest_addr)
                        param_count += 1

                # Verificar cantidad de parámetros
                if param_count != len(expected_params):
                    raise BabyDuckError("semantico",
                        f"Función '{func_name}' espera {len(expected_params)} argumentos pero se recibieron {param_count}")

                # Generar GOSUB
                start_addr = func_info["start_quad"]
                self._generate_quadruple("GOSUB", func_name, None, start_addr)

                # Si la función retorna un valor, guardarlo en temporal
                if func_info["type"] != "void":
                    func_return_addr = func_info["vars_table"]["__return__"]["direccion_virtual"]
                    temp_addr = self.mem_manager.get_virtual_address("temp", func_info["type"])
                    self._generate_quadruple("=", func_return_addr, None, temp_addr)

                    # Push del temporal a las pilas
                    self.operand_stack.append(temp_addr)
                    self.type_stack.append(func_info["type"])

            else:
                # Es una variable
                var_info = self._lookup_variable(var_name)
                if not var_info:
                    raise BabyDuckError("semantico",
                        f"Variable '{var_name}' no declarada")

                # Push de la variable
                self.operand_stack.append(var_info["direccion_virtual"])
                self.type_stack.append(var_info["type"])

        else:
            # Es una constante
            self.visit(ctx.cte())

        return None

    def visitCte(self, ctx):
        """
        Punto Neurálgico 9: Procesa constantes
        """
        if ctx.CTE_ENT():
            value = int(ctx.CTE_ENT().getText())
            const_type = "entero"
        elif ctx.CTE_FLOT():
            value = float(ctx.CTE_FLOT().getText())
            const_type = "flotante"

        # Agregar constante a la tabla y obtener dirección
        const_addr = self._add_constant(value, const_type)

        # Push de la constante
        self.operand_stack.append(const_addr)
        self.type_stack.append(const_type)

        return None