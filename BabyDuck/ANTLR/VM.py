from BabyDuckError import BabyDuckError

# configuracion de los rangos de memoria
GLOBAL_RANGES = range(1000, 3000)   # rangos para enteros y flotantes
LOCAL_RANGES  = range(3000, 5000)   # rangos para enteros y flotantes
TEMP_RANGES   = range(5000, 8000)   # rangos para enteros, flotantes y booleanos
CONST_RANGES  = range(8000, 11000)  # rangos para enteros, flotantes y strings

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
        """
        Asigna un valor a una direccion virtual
        """
        self.data[address] = value

class VirtualMachine:
    def __init__(self, quadruples, constants_map, dir_func):
        """
        Maquina virtual que ejecuta cuadruplos en tiempo de ejecucion
        """
        self.quadruples = quadruples
        self.dir_func = dir_func
        self.ip = 0  # Instruction Pointer
        
        # --- ESTRUCTURA DE MEMORIA ---
        self.mem_global = MemoryMap("Global")
        self.mem_const = MemoryMap("Constants")
        
        # Stack de ejecución (Lista de MemoryMaps)
        # Inicializamos con el scope 'global' o 'main'
        # limite de llamadas recursivas simultaneas
        self.MAX_STACK_SIZE = 1000 
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

    def _is_int_address(self, addr):
        """
        Devuelve True si la direccion pertenece a un segmento de enteros:
        global, local, temporal o constante
        """
        
        return (1000 <= addr < 2000 or 
                3000 <= addr < 4000 or 
                5000 <= addr < 6000 or 
                8000 <= addr < 9000)

    def get_value(self, address):
        """
        Busca la direccion y valida inicialización
        """
        val = None
        scope_name = ""


        if address in CONST_RANGES:
            val = self.mem_const.get(address)
            scope_name = "Constant"
        elif address in GLOBAL_RANGES:
            val = self.mem_global.get(address)
            scope_name = "Global"
        
        # buscar direccion en locales y temporales del scope actual
        elif (address in LOCAL_RANGES) or (address in TEMP_RANGES):
            val = self.call_stack[-1].get(address)
            scope_name = "Local/Temp"
        
        return val

    def set_value(self, address, value):
        """
        Escribe un valor en la dirección correcta.
        """
        if address in GLOBAL_RANGES:
            self.mem_global.set(address, value)
            
        elif (address in LOCAL_RANGES) or (address in TEMP_RANGES):
            self.call_stack[-1].set(address, value)

    def execute(self):
        print(">>> INICIANDO MÁQUINA VIRTUAL <<<")
        total_quads = len(self.quadruples)

        
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
                    # validar division entre 0
                    if r_val == 0:
                        raise BabyDuckError("vm", "Error de ejecucion: Division entre cero detectada")

                    # para enteros la division es int(l_val // r_val)
                    # para flotantes la division es simplemente l_val / r_val
                    if self._is_int_address(res):
                        self.set_value(res, int(l_val // r_val))
                    else:
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
                    continue # no incrementar el ip, moverlo en su lugar

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
                    
                    # Instanciar nuevo mapa de memoria pero NO hacer push todavía
                    self.mem_pending = MemoryMap(f"Scope_{func_name}")

                case 'PARAMETER':
                    # left: dirección origen (scope actual)
                    # res: dirección destino (parametro en scope pendiente)
                    
                    val = self.get_value(left)
                    # Escribimos directo en el mapa pendiente
                    self.mem_pending.set(res, val)

                case 'GOSUB':
                    func_start_addr = res
                    
                    if len(self.call_stack) >= self.MAX_STACK_SIZE:
                        raise BabyDuckError("vm", f"Stack Overflow: Se excedió el límite de {self.MAX_STACK_SIZE} llamadas recursivas")

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
                    self.call_stack.pop()
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
                        self.call_stack[-2].set(res, ret_val)

                    # El RETURN actúa también como fin de función
                    self.call_stack.pop()
                    self.ip = self.jump_stack.pop()
                    continue

                # ==================================
                #       FIN DEL PROGRAMA
                # ==================================
                case 'END':
                    print("\n>>> EJECUCIÓN FINALIZADA CON ÉXITO <<<")
                    return # regresar a compiler.py

                case _:
                    raise BabyDuckError("vm", f"OpCode desconocido: {op_code}")

            # Incrementar IP si no hubo saltos
            self.ip += 1