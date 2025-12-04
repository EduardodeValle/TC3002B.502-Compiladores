from BabyDuckError import BabyDuckError

class MemoryManager:
    def __init__(self):
        self.memory_map = {
            "global_entero":   {"start": 1000, "end": 1999},
            "global_flotante": {"start": 2000, "end": 2999},
            "local_entero":    {"start": 3000, "end": 3999},
            "local_flotante":  {"start": 4000, "end": 4999},
            "temp_entero":     {"start": 5000, "end": 5999},
            "temp_flotante":   {"start": 6000, "end": 6999},
            "temp_booleano":   {"start": 7000, "end": 7999},
            "const_entero":    {"start": 8000, "end": 8999},
            "const_flotante":  {"start": 9000, "end": 9999},
            "const_string":    {"start": 10000, "end": 10999}
        }

        self.counters = {key: val['start'] for key, val in self.memory_map.items()}

    def get_virtual_address(self, scope: str, var_type: str) -> int:
        """Genera direccion virtual basada en scope y tipo"""
        mem_key = f"{scope}_{var_type}"

        if mem_key not in self.counters:
            raise BabyDuckError("direcciones virtuales", f"Error: se intento asignar una direccion para {var_type} en {scope}")

        current_addr = self.counters[mem_key]
        limit = self.memory_map[mem_key]['end']

        if current_addr >= limit:
            raise BabyDuckError("direcciones virtuales", f"Se agoto el rango de direcciones virtuales en el scope {scope} para {var_type}")

        self.counters[mem_key] += 1

        return current_addr

    def reset_local_memory(self):
        """Reinicia contadores de memoria local y temporal"""
        print("--- Reiniciando memoria Local y Temporal para nueva funcion ---")
        reset_keys = ['local_entero', 'local_flotante', 'temp_entero', 'temp_flotante', 'temp_booleano']

        for key in reset_keys:
            self.counters[key] = self.memory_map[key]['start']
