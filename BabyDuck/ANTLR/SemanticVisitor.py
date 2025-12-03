from BabuDuckError import BabyDuckError
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
        self.constant_table = {}
        
        # --- DIRECTORIO DE FUNCIONES (TABLA DE SÍMBOLOS) ---
        # Inicializamos con el scope 'global' ya listo
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

    # helper functions para el directorio de funciones y tabla de simbolos

    def _create_function_entry(self, return_type, start_quad):
        """
        Crea el template vacío para una nueva función.
        """
        return {
            "type": return_type,
            "start_quad": start_quad,
            "vars_table": {},
            "param_signature": [], # Lista ordenada de tipos de parámetros (ej: ['int', 'float'])
            "resources": {         # Cantidad de recursos que necesitará la VM
                "local_entero": 0, 
                "local_flotante": 0, 
                "temp_entero": 0, 
                "temp_flotante": 0, 
                "temp_booleanoeanoeano": 0
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
            "temp_booleanoeano": self.mem_manager.counters['temp_booleanoeano'] - self.mem_manager.memory_map['temp_booleanoeano']['start'],
        }

        # Guardamos esto en el DirFunc de la función actual
        self.dir_func[self.current_scope]["resources"] = used_resources
        
        # Insertar cuádruplo ENDFUNC
        self.quadruples.append(("ENDFUNCTION", None, None, None))
        
        # Limpiar tabla de temporales si usas una aparte, y regresar scope a global si es necesario
        # (Aunque típicamente en ANTLR simplemente sales del nodo y el scope cambia cuando entras a otra func)
        self.current_scope = "global"

    def _create_var_entry(self, var_type, virtual_address):
        """
        Crea el template para una variable (sea local o global).
        """
        return {
            "type": var_type,
            "direccion_virtual": virtual_address
        }

    def _declare_variable(self, var_name, var_type):
        """
        Registra una variable en el scope actual (Global o Función).
        """
        current_vars = self.dir_func[self.current_scope]["vars_table"]
        
        if var_name in current_vars:
            raise BabyDuckError("semantico", f"La variable '{var_name}' ya fue declarada en el scope '{self.current_scope}'.")

        # 1. Pedir dirección virtual al MemoryManager
        scope_type = "global" if self.current_scope == "global" else "local"
        virtual_addr = self.mem_manager.get_virtual_address(scope_type, var_type)
        

        # 2. Guardar en la tabla
        current_vars[var_name] = self._create_var_entry(var_type, virtual_addr)

    # Otros helper functions

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