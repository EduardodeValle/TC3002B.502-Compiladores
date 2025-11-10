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
    
    def __init__(self, name, return_type='nula'):
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