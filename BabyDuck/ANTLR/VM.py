import sys

# configuracion de los rangos de memoria
GLOBAL_RANGES = range(1000, 3000)   # rangos para enteros y flotantes
LOCAL_RANGES  = range(3000, 5000)   # rangos para enteros y flotantes
TEMP_RANGES   = range(5000, 8000)   # rangos para enteros, flotantes y booleanos
CONST_RANGES  = range(8000, 10000)  # rangos para enteros y flotantes

# limite de llamadas recursivas simultaneas
MAX_STACK_SIZE = 1000 

class MemoryMap:
    """
    Un segmento de memoria por scope global o local
    """
    def __init__(self, name):
        self.name = name
        self.data = {}

    def get(self, address):
        """
        Retorna el valor de la direccion virtual
        """

        return self.data[address]

    def set(self, address, value):
        self.data[address] = value

    def __repr__(self):
        return f"<{self.name} Mem | Size: {len(self.data)}>"

class VirtualMachine:
    def __init__(self, quadruples, constants_map, dir_func):
        """
        :param quadruples: Lista de tuplas (op, left, right, res)
        :param constants_map: Diccionario { addr: val }
        :param dir_func: Directorio de funciones (necesario para ERA)
        """
        self.quadruples = quadruples
        self.dir_func = dir_func
        self.ip = 0  # Instruction Pointer
        
        # --- ESTRUCTURA DE MEMORIA ---
        self.mem_global = MemoryMap("Global")
        self.mem_const = MemoryMap("Constants")
        
        # Stack de ejecución (Lista de MemoryMaps)
        # Inicializamos con el scope 'global' o 'main'
        self.call_stack = [MemoryMap("Main_Scope")] 
        
        # Pila de saltos para retornos (GOSUB)
        self.jump_stack = []
        
        # Memoria temporal para preparar nuevas llamadas
        self.mem_pending = None 

        # Cargar constantes previamente compiladas
        self._load_constants(constants_map)

    def _load_constants(self, constants_map):
        for addr, val in constants_map.items():
            self.mem_const.set(addr, val)

    def get_value(self, address):
        """
        Rutea la dirección y valida inicialización.
        """
        val = None
        scope_name = ""

        # 1. Constantes
        if address in CONST_RANGES:
            val = self.mem_const.get(address)
            scope_name = "Constant"
        
        # 2. Globales
        elif address in GLOBAL_RANGES:
            val = self.mem_global.get(address)
            scope_name = "Global"
        
        # 3. Locales y Temporales (Stack Actual)
        elif (address in LOCAL_RANGES) or (address in TEMP_RANGES):
            if not self.call_stack:
                raise RuntimeError("Stack Underflow: Intento de acceso sin Stack Frame.")
            val = self.call_stack[-1].get(address)
            scope_name = "Local/Temp"
        
        else:
            raise RuntimeError(f"Segmentation Fault: Dirección {address} inválida.")

        # --- VALIDACIÓN: VARIABLE NO INICIALIZADA ---
        if val is None:
            raise RuntimeError(f"Error de Ejecución: Uso de variable no inicializada en dirección {address} ({scope_name}).")
        
        return val

    def set_value(self, address, value):
        """
        Escribe un valor en la dirección correcta.
        """
        if address in GLOBAL_RANGES:
            self.mem_global.set(address, value)
            
        elif (address in LOCAL_RANGES) or (address in TEMP_RANGES):
            if not self.call_stack:
                raise RuntimeError("Stack Underflow: No hay memoria local activa.")
            self.call_stack[-1].set(address, value)
            
        elif address in CONST_RANGES:
            raise RuntimeError("Error de Ejecución: Intento de escritura en Constante.")
        else:
            raise RuntimeError(f"Segmentation Fault: Dirección escritura {address} inválida.")

    def execute(self):
        print(">>> INICIANDO MÁQUINA VIRTUAL <<<")
        total_quads = len(self.quadruples)

        try:
            while self.ip < total_quads:
                op_code, left, right, res = self.quadruples[self.ip]

                match op_code:
                    # ==================================
                    #       ARITMÉTICA BÁSICA
                    # ==================================
                    case '+':
                        l_val = self.get_value(left)
                        r_val = self.get_value(right)
                        self.set_value(res, l_val + r_val)

                    case '-':
                        l_val = self.get_value(left)
                        r_val = self.get_value(right)
                        self.set_value(res, l_val - r_val)

                    case '*':
                        l_val = self.get_value(left)
                        r_val = self.get_value(right)
                        self.set_value(res, l_val * r_val)

                    case '/':
                        l_val = self.get_value(left)
                        r_val = self.get_value(right)
                        # --- VALIDACIÓN: DIVISIÓN ENTRE CERO ---
                        if r_val == 0:
                            raise ZeroDivisionError("División entre cero detectada.")
                        # Si manejas enteros y floats, Python se encarga del tipo resultante
                        # Si tu lenguaje es estricto con enteros, usa // para ints
                        self.set_value(res, l_val / r_val)

                    # ==================================
                    #       LÓGICA / COMPARACIÓN
                    # ==================================
                    case '>':
                        self.set_value(res, self.get_value(left) > self.get_value(right))
                    case '<':
                        self.set_value(res, self.get_value(left) < self.get_value(right))
                    case '==':
                        self.set_value(res, self.get_value(left) == self.get_value(right))
                    case '!=':
                        self.set_value(res, self.get_value(left) != self.get_value(right))

                    # ==================================
                    #       ASIGNACIÓN
                    # ==================================
                    case '=':
                        val = self.get_value(left)
                        self.set_value(res, val)
                    
                    case 'unario+':
                        val = self.get_value(left)
                        self.set_value(res, +val)

                    case 'unario-':
                        val = self.get_value(left)
                        self.set_value(res, -val)

                    # ==================================
                    #       ENTRADA / SALIDA
                    # ==================================
                    case 'PRINT':
                        # Imprimir el valor (res contiene la dirección a imprimir)
                        # Nota: En algunos diseños el dato está en 'res', en otros en 'left'.
                        # Ajusta según tu generador de cuádruplos. Asumiré que está en 'res'.
                        val_to_print = self.get_value(res) 
                        print(f"> {val_to_print}")

                    # ==================================
                    #       CONTROL DE FLUJO
                    # ==================================
                    case 'GOTO':
                        self.ip = res
                        continue # Evita el ip += 1 del final

                    case 'GOTOF':
                        condition = self.get_value(left)
                        if not condition: # Si es Falso
                            self.ip = res
                            continue

                    # ==================================
                    #       FUNCIONES (ERA / GOSUB)
                    # ==================================
                    case 'ERA':
                        func_name = left
                        # Verificar si existe en directorio
                        if func_name not in self.dir_func:
                            raise RuntimeError(f"Función '{func_name}' no encontrada en directorio.")
                        
                        # Instanciar nuevo mapa de memoria pero NO hacer push todavía
                        self.mem_pending = MemoryMap(f"Scope_{func_name}")

                    case 'PARAMETER':
                        # left: dirección origen (scope actual)
                        # res: dirección destino (parametro en scope pendiente)
                        if self.mem_pending is None:
                            raise RuntimeError("Instrucción PARAMETER sin ERA previo.")
                        
                        val = self.get_value(left)
                        # Escribimos directo en el mapa pendiente
                        self.mem_pending.set(res, val)

                    case 'GOSUB':
                        func_start_addr = res
                        
                        # --- VALIDACIÓN: STACK OVERFLOW ---
                        if len(self.call_stack) >= MAX_STACK_SIZE:
                            raise RuntimeError(f"STACK OVERFLOW: Se excedió el límite de {MAX_STACK_SIZE} llamadas recursivas.")

                        # Guardar dirección de retorno
                        self.jump_stack.append(self.ip + 1)
                        
                        # Activar el nuevo contexto
                        if self.mem_pending:
                            self.call_stack.append(self.mem_pending)
                            self.mem_pending = None
                        else:
                            # Caso borde: funcion sin params podría no haber tenido ERA (depende de tu compilador)
                            # Creamos un scope vacío por seguridad
                            self.call_stack.append(MemoryMap("Scope_Void"))

                        self.ip = func_start_addr
                        continue

                    case 'ENDFUNCTION':
                        # Liberar memoria local
                        self.call_stack.pop()
                        # Regresar instrucción
                        self.ip = self.jump_stack.pop()
                        continue

                    case 'RETURN':
                        # left: valor a retornar
                        # res: dirección donde guardar el retorno (usualmente una Global o Temp del Caller)
                        ret_val = self.get_value(left)
                        
                        # Lógica de asignación del retorno:
                        # Si res es Global, escribimos directo.
                        if res in GLOBAL_RANGES:
                            self.mem_global.set(res, ret_val)
                        else:
                            # Si res es Temp, debe pertenecer al CALLER (el scope anterior en el stack)
                            # Necesitamos escribir en stack[-2] porque stack[-1] está a punto de morir.
                            if len(self.call_stack) > 1:
                                self.call_stack[-2].set(res, ret_val)
                            else:
                                raise RuntimeError("RETURN fuera de contexto de función.")

                        # El RETURN actúa también como fin de función
                        self.call_stack.pop()
                        self.ip = self.jump_stack.pop()
                        continue

                    # ==================================
                    #       FIN DEL PROGRAMA
                    # ==================================
                    case 'END':
                        print("\n>>> EJECUCIÓN FINALIZADA CON ÉXITO <<<")
                        sys.exit(0)

                    case _:
                        raise RuntimeError(f"OpCode desconocido: {op_code}")

                # Incrementar IP si no hubo saltos
                self.ip += 1

        except Exception as e:
            print(f"\n!!! ERROR DE EJECUCIÓN !!!")
            print(f"Instrucción fallida en Cuádruplo #{self.ip}: {self.quadruples[self.ip]}")
            print(f"Causa: {e}")
            sys.exit(1)