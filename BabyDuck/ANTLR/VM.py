from BabyDuckError import BabyDuckError

GLOBAL_RANGES = range(1000, 3000)
LOCAL_RANGES  = range(3000, 5000)
TEMP_RANGES   = range(5000, 8000)
CONST_RANGES  = range(8000, 11000)

class MemoryMap:
    """Segmento de memoria por scope"""
    def __init__(self, name):
        self.name = name
        self.data = {}

    def get(self, address):
        if address not in self.data:
            raise BabyDuckError("vm",
                f"Error de ejecucion: Se intento acceder a una variable no inicializada (direccion {address})")
        return self.data[address]

    def set(self, address, value):
        self.data[address] = value

class VirtualMachine:
    def __init__(self, quadruples, constants_map):
        """Ejecuta cuadruplos en tiempo de ejecucion"""
        self.quadruples = quadruples
        self.ip = 0

        self.mem_global = MemoryMap("Global")
        self.mem_const = MemoryMap("Constants")

        self.MAX_STACK_SIZE = 1000
        self.call_stack = [MemoryMap("Main_Scope")]
        self.jump_stack = []
        self.mem_pending_stack = []

        self._load_constants(constants_map)

    def _load_constants(self, constants_map):
        for addr, val in constants_map.items():
            self.mem_const.set(addr, val)

    def _is_int_address(self, addr):
        return (1000 <= addr < 2000 or
                3000 <= addr < 4000 or
                5000 <= addr < 6000 or
                8000 <= addr < 9000)

    def get_value(self, address):
        val = None
        scope_name = ""

        if address in CONST_RANGES:
            val = self.mem_const.get(address)
            scope_name = "Constant"
        elif address in GLOBAL_RANGES:
            val = self.mem_global.get(address)
            scope_name = "Global"
        elif (address in LOCAL_RANGES) or (address in TEMP_RANGES):
            val = self.call_stack[-1].get(address)
            scope_name = "Local/Temp"

        return val

    def set_value(self, address, value):
        if address in GLOBAL_RANGES:
            self.mem_global.set(address, value)
        elif (address in LOCAL_RANGES) or (address in TEMP_RANGES):
            self.call_stack[-1].set(address, value)

    def execute(self):
        print(">>> INICIANDO MAQUINA VIRTUAL <<<")
        total_quads = len(self.quadruples)

        while self.ip < total_quads:
            op_code, left, right, res = self.quadruples[self.ip]

            match op_code:
                case "+":
                    l_val = self.get_value(left)
                    r_val = self.get_value(right)
                    self.set_value(res, l_val + r_val)

                case "-":
                    l_val = self.get_value(left)
                    r_val = self.get_value(right)
                    self.set_value(res, l_val - r_val)

                case "*":
                    l_val = self.get_value(left)
                    r_val = self.get_value(right)
                    self.set_value(res, l_val * r_val)

                case "/":
                    l_val = self.get_value(left)
                    r_val = self.get_value(right)
                    if r_val == 0:
                        raise BabyDuckError("vm", "Error de ejecucion: Division entre cero detectada")

                    if self._is_int_address(res):
                        self.set_value(res, int(l_val // r_val))
                    else:
                        self.set_value(res, l_val / r_val)
                case ">":
                    self.set_value(res, self.get_value(left) > self.get_value(right))
                case "<":
                    self.set_value(res, self.get_value(left) < self.get_value(right))
                case "==":
                    self.set_value(res, self.get_value(left) == self.get_value(right))
                case "!=":
                    self.set_value(res, self.get_value(left) != self.get_value(right))

                case "=":
                    val = self.get_value(left)
                    self.set_value(res, val)
                
                case "unario+":
                    val = self.get_value(left)
                    self.set_value(res, +val)

                case "unario-":
                    val = self.get_value(left)
                    self.set_value(res, -val)

                case "PRINT":
                    val_to_print = self.get_value(res)
                    print(f"> {val_to_print}")

                case "GOTO":
                    self.ip = res
                    continue

                case "GOTOF":
                    condition = self.get_value(left)
                    if not condition:
                        self.ip = res
                        continue
                case "ERA":
                    func_name = left
                    self.mem_pending_stack.append(MemoryMap(f"Scope_{func_name}"))

                case "PARAMETER":
                    val = self.get_value(left)
                    self.mem_pending_stack[-1].set(res, val)

                case "GOSUB":
                    func_start_addr = res

                    if len(self.call_stack) >= self.MAX_STACK_SIZE:
                        raise BabyDuckError("vm", f"Stack Overflow: Se excedio el limite de {self.MAX_STACK_SIZE} llamadas recursivas")

                    self.jump_stack.append(self.ip + 1)

                    if self.mem_pending_stack:
                        self.call_stack.append(self.mem_pending_stack.pop())
                    else:
                        self.call_stack.append(MemoryMap("Scope_Void"))

                    self.ip = func_start_addr
                    continue

                case "ENDFUNCTION":
                    self.call_stack.pop()
                    self.ip = self.jump_stack.pop()
                    continue

                case "RETURN":
                    ret_val = self.get_value(left)

                    if res in GLOBAL_RANGES:
                        self.mem_global.set(res, ret_val)
                    else:
                        self.call_stack[-2].set(res, ret_val)

                    self.call_stack.pop()
                    self.ip = self.jump_stack.pop()
                    continue

                case "END":
                    print("\n>>> EJECUCION FINALIZADA CON EXITO <<<")
                    return

                case _:
                    raise BabyDuckError("vm", f"OpCode desconocido: {op_code}")

            self.ip += 1