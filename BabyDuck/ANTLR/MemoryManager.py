from BabuDuckError import BabyDuckError

class MemoryError(Exception):
    """Excepción personalizada para cuando se agota la memoria virtual."""
    pass

class MemoryManager:
    def __init__(self):
        # Configuración de los rangos de memoria (PARAMETRIZABLE)
        # Formato: [Inicio, Limite_Superior (exclusivo)]
        # Puedes modificar estos números para aumentar/disminuir el rango
        self.memory_map = {
            # --- GLOBAL (No se reinicia) ---
            'global_int':   {'start': 1000, 'end': 1999},
            'global_float': {'start': 2000, 'end': 2999},
            
            # --- LOCAL (Se reinicia por función) ---
            'local_int':    {'start': 3000, 'end': 3999},
            'local_float':  {'start': 4000, 'end': 4999},
            
            # --- TEMPORAL (Se reinicia por función) ---
            'temp_int':     {'start': 5000, 'end': 5999},
            'temp_float':   {'start': 6000, 'end': 6999},
            'temp_bool':    {'start': 7000, 'end': 7999}, # Solo existen como temporales
            
            # --- CONSTANTES (No se reinicia) ---
            'const_int':    {'start': 8000, 'end': 8999},
            'const_float':  {'start': 9000, 'end': 9999}
        }

        # Inicializar contadores en el valor de inicio de cada rango
        self.counters = {key: val['start'] for key, val in self.memory_map.items()}

    def _print_memory_status(self):
        """
        Helper function para debuggear el estado actual de la memoria.
        """
        print("\nEstado actual de contadores de Memoria Virtual:")
        for key, val in self.counters.items():
            used = val - self.memory_map[key]['start']
            total = self.memory_map[key]['end'] - self.memory_map[key]['start']
            print(f"  {key:<12}: {val} (Usados: {used}/{total})")

    def get_virtual_address(self, scope: str, var_type: str) -> int:
        """
        Genera una direccion virtual basada en el scope y el tipo.
        
        scope: 'global', 'local', 'temp', 'const'
        var_type: 'int', 'float', 'bool'
        """
        mem_key = f"{scope}_{var_type}"

        if mem_key not in self.counters:
            raise BabyDuckError("direcciones virtuales", f"Error: se intento asignar una direccion invalida: {mem_key}")

        # obtener dirección actual y limites
        current_addr = self.counters[mem_key]
        limit = self.memory_map[mem_key]['end']

        if current_addr >= limit:
            raise BabyDuckError("direcciones virtuales", f"Se agoto el rango de direcciones virtuales en el scope {scope} para {mem_key}")

        # actualizar el contador para la siguiente variable
        self.counters[mem_key] += 1

        return current_addr

    def reset_local_memory(self):
        """
        Reinicia los contadores de memoria local y temporal, se llama
        cada vez que se cambia de scope
        """
        print("--- Reiniciando memoria Local y Temporal para nueva función ---")
        reset_keys = ['local_int', 'local_float', 'temp_int', 'temp_float', 'temp_bool']
        
        for key in reset_keys:
            self.counters[key] = self.memory_map[key]['start']