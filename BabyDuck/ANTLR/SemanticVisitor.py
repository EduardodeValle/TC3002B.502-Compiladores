from BabyDuckError import BabyDuckError
from BabyDuckParser import BabyDuckParser
from BabyDuckVisitor import BabyDuckVisitor

from MemoryManager import MemoryManager
from semantic_cube import semantic_cube

class SemanticVisitor(BabyDuckVisitor):
    def __init__(self):
        self.quadruples = []
        self.operand_stack = []
        self.type_stack = []
        self.operator_stack = []
        self.jump_stack = []
        self.pending_jump = None

        self.cube = semantic_cube
        self.mem_manager = MemoryManager()
        self.constant_table = {}

        self.dir_func = {
            "global": {
                "type": "void",
                "start_quad": 0,
                "vars_table": {},
                "param_signature": [],
                "param_addresses": [],
                "resources": {}
            }
        }

        self.current_scope = "global"
        self.current_id = None
        self.current_function_has_return = False

    def _create_function_entry(self, return_type, start_quad):
        """Crea entrada para nueva función"""
        return {
            "type": return_type,
            "start_quad": start_quad,
            "vars_table": {},
            "param_signature": [],
            "param_addresses": [],
            "resources": {
                "local_entero": 0,
                "local_flotante": 0,
                "temp_entero": 0,
                "temp_flotante": 0,
                "temp_booleano": 0
            }
        }

    def _declare_function(self, func_name, return_type, start_quad):
        """Registra función y cambia scope"""
        if func_name in self.dir_func:
            raise BabyDuckError("semantico", f"La funcion '{func_name}' ya existe")

        self.dir_func[func_name] = self._create_function_entry(return_type, start_quad)
        self.current_scope = func_name
        self.mem_manager.reset_local_memory()

    def _end_function_logic(self):
        """Calcula recursos usados y finaliza función"""
        used_resources = {
            "local_entero": self.mem_manager.counters['local_entero'] - self.mem_manager.memory_map['local_entero']['start'],
            "local_flotante": self.mem_manager.counters['local_flotante'] - self.mem_manager.memory_map['local_flotante']['start'],
            "temp_entero": self.mem_manager.counters['temp_entero'] - self.mem_manager.memory_map['temp_entero']['start'],
            "temp_flotante": self.mem_manager.counters['temp_flotante'] - self.mem_manager.memory_map['temp_flotante']['start'],
            "temp_booleano": self.mem_manager.counters['temp_booleano'] - self.mem_manager.memory_map['temp_booleano']['start'],
        }

        self.dir_func[self.current_scope]["resources"] = used_resources
        self.quadruples.append(("ENDFUNCTION", None, None, None))
        self.current_scope = "global"

    def _create_var_entry(self, var_type, virtual_address, initialized=False):
        """Crea entrada para variable"""
        return {
            "type": var_type,
            "direccion_virtual": virtual_address,
            "initialized": initialized
        }

    def _declare_variable(self, var_name, var_type, is_param=False):
        """Registra variable en scope actual"""
        current_vars = self.dir_func[self.current_scope]["vars_table"]

        if var_name in current_vars:
            raise BabyDuckError("semantico", f"La variable '{var_name}' ya fue declarada en el scope '{self.current_scope}'.")

        scope_type = "global" if self.current_scope == "global" else "local"
        virtual_addr = self.mem_manager.get_virtual_address(scope_type, var_type)
        current_vars[var_name] = self._create_var_entry(var_type, virtual_addr, initialized=is_param)

        return virtual_addr

    def _lookup_variable(self, var_name):
        """Busca variable en scope local, luego global"""
        current_vars = self.dir_func[self.current_scope]["vars_table"]
        if var_name in current_vars:
            return current_vars[var_name]

        if self.current_scope != "global":
            global_vars = self.dir_func["global"]["vars_table"]
            if var_name in global_vars:
                return global_vars[var_name]

        return None

    def _mark_variable_initialized(self, var_name):
        """Marca variable como inicializada"""
        current_vars = self.dir_func[self.current_scope]["vars_table"]
        if var_name in current_vars:
            current_vars[var_name]["initialized"] = True
        elif self.current_scope != "global":
            global_vars = self.dir_func["global"]["vars_table"]
            if var_name in global_vars:
                global_vars[var_name]["initialized"] = True

    def _add_constant(self, value, const_type):
        """Agrega constante a tabla y retorna dirección virtual"""
        const_key = (value, const_type)

        if const_key in self.constant_table:
            return self.constant_table[const_key]["direccion_virtual"]

        scope_type = "const"
        virtual_addr = self.mem_manager.get_virtual_address(scope_type, const_type)

        self.constant_table[const_key] = {
            "value": value,
            "type": const_type,
            "direccion_virtual": virtual_addr
        }

        return virtual_addr

    def _generate_quadruple(self, operator, left_operand, right_operand, result):
        """Genera cuádruplo y retorna su índice"""
        quad = (operator, left_operand, right_operand, result)
        self.quadruples.append(quad)
        return len(self.quadruples) - 1

    def _fill_quadruple(self, quad_index, result_value):
        """Rellena cuádruplo pendiente"""
        operator, left, right, _ = self.quadruples[quad_index]
        self.quadruples[quad_index] = (operator, left, right, result_value)

    def _solve_pending_operations(self, allowed_operators):
        """Resuelve operaciones según precedencia y genera cuádruplos"""
        while (self.operator_stack and
               self.operator_stack[-1] != "(" and
               self.operator_stack[-1] in allowed_operators):

            operator = self.operator_stack.pop()
            right_operand = self.operand_stack.pop()
            right_type = self.type_stack.pop()
            left_operand = self.operand_stack.pop()
            left_type = self.type_stack.pop()

            try:
                result_type = self.cube[left_type][right_type][operator]
            except KeyError:
                raise BabyDuckError("semantico",
                    f"Operación inválida: {left_type} {operator} {right_type}")

            if result_type == "error":
                raise BabyDuckError("semantico",
                    f"Operación inválida: {left_type} {operator} {right_type}")

            temp_addr = self.mem_manager.get_virtual_address("temp", result_type)
            self._generate_quadruple(operator, left_operand, right_operand, temp_addr)

            self.operand_stack.append(temp_addr)
            self.type_stack.append(result_type)

    def get_constants_for_vm(self):
        """Retorna diccionario {dirección: valor} para VM"""
        constants_map = {}
        for const_info in self.constant_table.values():
            addr = const_info["direccion_virtual"]
            value = const_info["value"]
            constants_map[addr] = value
        return constants_map

    def visitPrograma(self, ctx):
        """PN 1-3: GOTO a main, rellenar al encontrar inicio, END al fin"""
        self.pending_jump = self._generate_quadruple("GOTO", None, None, None)

        if ctx.vars_():
            self.visit(ctx.vars_())

        for func in ctx.funcs():
            self.visit(func)

        self._fill_quadruple(self.pending_jump, len(self.quadruples))
        self.current_scope = "global"
        self.visit(ctx.cuerpo())
        self._generate_quadruple("END", None, None, None)

        return None

    def visitVars(self, ctx):
        """PN 4: Procesar declaraciones de variables"""
        for declaracion in ctx.declarar_variables():
            self.visit(declaracion)
        return None

    def visitDeclarar_variables(self, ctx):
        tipo_ctx = ctx.tipo()
        var_type = self.visit(tipo_ctx)
        ids_ctx = ctx.declarar_ids()
        var_names = self.visit(ids_ctx)

        for var_name in var_names:
            self._declare_variable(var_name, var_type, is_param=False)

        return None

    def visitDeclarar_ids(self, ctx):
        var_names = []
        for id_token in ctx.ID():
            var_names.append(id_token.getText())
        return var_names

    def visitTipo(self, ctx):
        if ctx.ENTERO():
            return "entero"
        elif ctx.FLOTANTE():
            return "flotante"
        return None

    def visitFuncs(self, ctx):
        """PN 5-9: Procesamiento completo de funciones"""
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
        """PN 7: Procesar parámetros como variables locales"""
        ids = ctx.ID()
        tipos = ctx.tipo()

        for i in range(len(ids)):
            param_name = ids[i].getText()
            param_type = self.visit(tipos[i])
            param_addr = self._declare_variable(param_name, param_type, is_param=True)

            self.dir_func[self.current_scope]["param_signature"].append(param_type)
            self.dir_func[self.current_scope]["param_addresses"].append(param_addr)

        return None

    def visitDevuelve(self, ctx):
        """PN 8: Procesar token devolver"""
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

    def visitCuerpo(self, ctx):
        for estatuto in ctx.estatuto():
            self.visit(estatuto)
        return None

    def visitEstatuto(self, ctx):
        if ctx.continuacion_de_estatuto_id():
            var_name = ctx.ID().getText()
            self.current_id = var_name
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
            for estatuto in ctx.estatuto():
                self.visit(estatuto)
        return None

    def visitContinuacion_de_estatuto_id(self, ctx):
        """PN 12, 20-22: Asignación o llamada a función"""
        if ctx.ASIGNACION():
            var_name = self.current_id
            var_info = self._lookup_variable(var_name)
            if not var_info:
                raise BabyDuckError("semantico",
                    f"Variable '{var_name}' no declarada")

            self.visit(ctx.expresion(0))

            expr_type = self.type_stack.pop()
            expr_addr = self.operand_stack.pop()
            var_type = var_info["type"]

            try:
                assignment_result = self.cube[var_type][expr_type]["="]
            except KeyError:
                assignment_result = "error"

            if assignment_result == "error":
                raise BabyDuckError("semantico",
                    f"No se puede asignar '{expr_type}' a variable de tipo '{var_type}'")

            var_addr = var_info["direccion_virtual"]
            self._generate_quadruple("=", expr_addr, None, var_addr)
            self._mark_variable_initialized(var_name)

        else:
            func_name = self.current_id

            if func_name not in self.dir_func:
                raise BabyDuckError("semantico",
                    f"Función '{func_name}' no declarada")

            func_info = self.dir_func[func_name]
            self._generate_quadruple("ERA", func_name, None, None)

            param_count = 0
            expected_params = func_info["param_signature"]
            param_addresses = func_info["param_addresses"]

            # Poner un paréntesis falso para evitar que se resuelvan operaciones pendientes
            # mientras se procesan los argumentos de la función
            self.operator_stack.append("(")

            if ctx.expresion():
                for expr_ctx in ctx.expresion():
                    self.visit(expr_ctx)

                    if param_count >= len(expected_params):
                        raise BabyDuckError("semantico",
                            f"Demasiados argumentos para función '{func_name}'")

                    arg_type = self.type_stack.pop()
                    arg_addr = self.operand_stack.pop()
                    expected_type = expected_params[param_count]

                    if arg_type != expected_type:
                        raise BabyDuckError("semantico",
                            f"Argumento {param_count + 1} de '{func_name}': se esperaba '{expected_type}' pero se obtuvo '{arg_type}'")

                    param_dest_addr = param_addresses[param_count]
                    self._generate_quadruple("PARAMETER", arg_addr, None, param_dest_addr)
                    param_count += 1

            # Remover el paréntesis falso
            if self.operator_stack and self.operator_stack[-1] == "(":
                self.operator_stack.pop()

            if param_count != len(expected_params):
                raise BabyDuckError("semantico",
                    f"Función '{func_name}' espera {len(expected_params)} argumentos pero se recibieron {param_count}")

            start_addr = func_info["start_quad"]
            self._generate_quadruple("GOSUB", func_name, None, start_addr)

            if func_info["type"] != "void":
                func_return_addr = func_info["vars_table"]["__return__"]["direccion_virtual"]
                temp_addr = self.mem_manager.get_virtual_address("temp", func_info["type"])
                self._generate_quadruple("=", func_return_addr, None, temp_addr)

                self.operand_stack.append(temp_addr)
                self.type_stack.append(func_info["type"])

        return None

    def visitImprime(self, ctx):
        """PN 13: Generar cuádruplos PRINT"""
        self.visit(ctx.imprimir_elementos())
        return None

    def visitImprimir_elementos(self, ctx):
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

    def visitCondicion(self, ctx):
        """PN 14-16: Procesar if/else"""
        self.visit(ctx.expresion())

        expr_type = self.type_stack.pop()
        expr_addr = self.operand_stack.pop()

        if expr_type != "booleano":
            raise BabyDuckError("semantico",
                "La condición del 'si' debe ser una expresión booleana")

        gotof_index = self._generate_quadruple("GOTOF", expr_addr, None, None)
        self.jump_stack.append(gotof_index)

        self.visit(ctx.cuerpo(0))

        if len(ctx.cuerpo()) > 1:
            goto_index = self._generate_quadruple("GOTO", None, None, None)

            gotof_idx = self.jump_stack.pop()
            self._fill_quadruple(gotof_idx, len(self.quadruples))

            self.visit(ctx.cuerpo(1))

            self._fill_quadruple(goto_index, len(self.quadruples))
        else:
            gotof_idx = self.jump_stack.pop()
            self._fill_quadruple(gotof_idx, len(self.quadruples))

        return None

    def visitCiclo(self, ctx):
        """PN 17-19: Procesar while"""
        start_expr_index = len(self.quadruples)
        self.jump_stack.append(start_expr_index)

        self.visit(ctx.expresion())

        expr_type = self.type_stack.pop()
        expr_addr = self.operand_stack.pop()

        if expr_type != "booleano":
            raise BabyDuckError("semantico",
                "La condición del 'mientras' debe ser una expresión booleana")

        gotof_index = self._generate_quadruple("GOTOF", expr_addr, None, None)
        self.jump_stack.append(gotof_index)

        self.visit(ctx.cuerpo())

        gotof_idx = self.jump_stack.pop()
        start_idx = self.jump_stack.pop()

        self._generate_quadruple("GOTO", None, None, start_idx)
        self._fill_quadruple(gotof_idx, len(self.quadruples))

        return None

    def visitExpresion(self, ctx):
        """Procesa expresiones con operadores relacionales"""
        self.visit(ctx.exp(0))

        if len(ctx.exp()) > 1:
            if ctx.MAYOR_QUE():
                operator = ">"
            elif ctx.MENOR_QUE():
                operator = "<"
            elif ctx.DIFERENTE_DE():
                operator = "!="
            elif ctx.IGUAL_QUE():
                operator = "=="

            self.operator_stack.append(operator)
            self.visit(ctx.exp(1))
            self._solve_pending_operations([">", "<", "!=", "=="])

        return None

    def visitExp(self, ctx):
        """Procesa suma y resta"""
        self.visit(ctx.termino(0))

        for i in range(1, len(ctx.termino())):
            # Acceder al operador directamente desde children
            # Los children son: termino, operador, termino, operador, termino, ...
            # El operador entre termino(i-1) y termino(i) está en children[2*i - 1]
            operator_token = ctx.children[2*i - 1]
            if operator_token.getText() == '+':
                operator = "+"
            else:  # operator_token.getText() == '-'
                operator = "-"

            self.operator_stack.append(operator)
            self.visit(ctx.termino(i))
            self._solve_pending_operations(["+", "-"])

        return None

    def visitTermino(self, ctx):
        """Procesa multiplicación y división"""
        self.visit(ctx.factor(0))

        for i in range(1, len(ctx.factor())):
            # Acceder al operador directamente desde children
            # El operador entre factor(i-1) y factor(i) está en children[2*i - 1]
            operator_token = ctx.children[2*i - 1]
            if operator_token.getText() == '*':
                operator = "*"
            else:  # operator_token.getText() == '/'
                operator = "/"

            self.operator_stack.append(operator)
            self.visit(ctx.factor(i))
            self._solve_pending_operations(["*", "/"])

        return None

    def visitFactor(self, ctx):
        """Procesa factores con signos unarios y paréntesis"""
        if ctx.PARENTESIS_IZQUIERDO():
            self.operator_stack.append("(")
            self.visit(ctx.expresion())

            if self.operator_stack and self.operator_stack[-1] == "(":
                self.operator_stack.pop()

        elif ctx.MAS() or ctx.MENOS():
            self.visit(ctx.dato_o_llamada())

            if ctx.MENOS():
                operand = self.operand_stack.pop()
                operand_type = self.type_stack.pop()

                temp_addr = self.mem_manager.get_virtual_address("temp", operand_type)
                self._generate_quadruple("unario-", operand, None, temp_addr)

                self.operand_stack.append(temp_addr)
                self.type_stack.append(operand_type)

        else:
            self.visit(ctx.dato_o_llamada())

        return None

    def visitDato_o_llamada(self, ctx):
        """PN 9-11: Procesa ID, constantes o llamadas a función"""
        if ctx.ID():
            var_name = ctx.ID().getText()

            if ctx.PARENTESIS_IZQUIERDO():
                func_name = var_name

                if func_name not in self.dir_func:
                    raise BabyDuckError("semantico",
                        f"Función '{func_name}' no declarada")

                func_info = self.dir_func[func_name]
                self._generate_quadruple("ERA", func_name, None, None)

                param_count = 0
                expected_params = func_info["param_signature"]
                param_addresses = func_info["param_addresses"]

                # Poner un paréntesis falso para evitar que se resuelvan operaciones pendientes
                # mientras se procesan los argumentos de la función
                self.operator_stack.append("(")

                if ctx.expresion():
                    for expr_ctx in ctx.expresion():
                        self.visit(expr_ctx)

                        if param_count >= len(expected_params):
                            raise BabyDuckError("semantico",
                                f"Demasiados argumentos para función '{func_name}'")

                        arg_type = self.type_stack.pop()
                        arg_addr = self.operand_stack.pop()
                        expected_type = expected_params[param_count]

                        if arg_type != expected_type:
                            raise BabyDuckError("semantico",
                                f"Argumento {param_count + 1} de '{func_name}': se esperaba '{expected_type}' pero se obtuvo '{arg_type}'")

                        param_dest_addr = param_addresses[param_count]
                        self._generate_quadruple("PARAMETER", arg_addr, None, param_dest_addr)
                        param_count += 1

                # Remover el paréntesis falso
                if self.operator_stack and self.operator_stack[-1] == "(":
                    self.operator_stack.pop()

                if param_count != len(expected_params):
                    raise BabyDuckError("semantico",
                        f"Función '{func_name}' espera {len(expected_params)} argumentos pero se recibieron {param_count}")

                start_addr = func_info["start_quad"]
                self._generate_quadruple("GOSUB", func_name, None, start_addr)

                if func_info["type"] != "void":
                    func_return_addr = func_info["vars_table"]["__return__"]["direccion_virtual"]
                    temp_addr = self.mem_manager.get_virtual_address("temp", func_info["type"])
                    self._generate_quadruple("=", func_return_addr, None, temp_addr)

                    self.operand_stack.append(temp_addr)
                    self.type_stack.append(func_info["type"])

            else:
                var_info = self._lookup_variable(var_name)
                if not var_info:
                    raise BabyDuckError("semantico",
                        f"Variable '{var_name}' no declarada")

                self.operand_stack.append(var_info["direccion_virtual"])
                self.type_stack.append(var_info["type"])

        else:
            self.visit(ctx.cte())

        return None

    def visitCte(self, ctx):
        """PN 9: Procesa constantes"""
        if ctx.CTE_ENT():
            value = int(ctx.CTE_ENT().getText())
            const_type = "entero"
        elif ctx.CTE_FLOT():
            value = float(ctx.CTE_FLOT().getText())
            const_type = "flotante"

        const_addr = self._add_constant(value, const_type)

        self.operand_stack.append(const_addr)
        self.type_stack.append(const_type)

        return None