class Symbol:
    """
    Representa una entrada en la Tabla de Variables (una variable) 
    """
    
    def __init__(self, name, type, initialized=False):
        self.name = name
        self.type = type
        self.initialized = initialized

    def __str__(self):
        """
        Construcción de un mensaje para debugging
        """
        msg = "<", self.name, ": ", self.type, ",  init=", self.initialized, ">"
        return msg

class FuncInfo:
    """ 
    Representa una entrada en el directorio de funciones
    con metadatos de la función y su tabla de variables local
    """
    
    def __init__(self, name, return_type="nulo"):
        self.name = name              
        self.return_type = return_type
        self.param_types = []
        self.variables_table = {}

    def add_param(self, param_type):
        """ 
        Agrega un tipo de parámetro a la firma de la función.
        """
        self.param_types.append(param_type)

    def __str__(self):
        """
        Construcción de un mensaje para debugging
        """
        var_count = len(self.variables_table)
        msg = "[Func: ", self.name, ", Returns: ", self.return_type, ", Params: ", self.param_types, ", LocalVars: ", var_count, "]"
        return msg

class SymbolTableManager:
    """
    Gestiona el Directorio de Funciones y un puntero al scope actual,
    ya sea global o de función
    """
    
    def __init__(self):
        self.function_directory = {}
        self.current_scope = None # puntero al scope actual, apunta a una tabla de variables
        self.global_scope = None # puntero de acceso rápido al scope global

    def start_program(self):
        """
        Se llama al iniciar el programa para crear el scope global
        """

        # crear el scope global
        global_func_info = FuncInfo("global", "nulo")
        self.function_directory["global"] = global_func_info
        
        # establecer los punteros de scope
        self.global_scope = global_func_info.variables_table
        self.current_scope = global_func_info.variables_table

    def add_function(self, func_name, return_type):
        """
        Punto neurálgico al visitar <FUNCS> 
            - Crea la entrada de la función y la establece como scope actual
            - Devuelve False si la función ya existía y no hace nada
        """
        
        if func_name in self.function_directory:
            return False 
            
        func_info = FuncInfo(func_name, return_type)
        self.function_directory[func_name] = func_info        
        self.current_scope = func_info.variables_table
        return True

    def end_function(self):
        """ 
        Restaura el scope actual para que sea el global al terminar
        de visitar <FUNCS>
        """
        self.current_scope = self.global_scope

    