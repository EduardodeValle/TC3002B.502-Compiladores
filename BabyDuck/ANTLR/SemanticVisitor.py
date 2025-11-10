from BabuDuckError import BabyDuckError
from BabyDuckParser import BabyDuckParser
from BabyDuckVisitor import BabyDuckVisitor

from semantic_cube import semantic_cube

class SemanticVisitor(BabyDuckVisitor):
    def __init__(self):
        self.cube = semantic_cube

    def get_op_string(self, token_type):
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

    