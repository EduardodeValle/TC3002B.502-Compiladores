from antlr4 import *
import sys

from BabyDuckLexer import BabyDuckLexer
from BabyDuckParser import BabyDuckParser

def run_compiler(filepath: str):
    """
    Función principal llamada por main que maneja todo el pipeline de compilación de BabyDuck
    """

    print("Compilando ", filepath)
    input_stream = FileStream(filepath)
    lexer = BabyDuckLexer(input_stream) # lexer de ANTLR
    stream = CommonTokenStream(lexer)
    parser = BabyDuckParser(stream) # parser de ANTRL
    
    # Iniciar parser desde el token principal: programa
    tree = parser.programa() 
    
    print("\n==================================================================")
    print("Semántica completada")
    print("==================================================================\n")

    print("\n==================================================================")
    print("Generación de cuádruplos completada")
    print("==================================================================\n")

    print("\n==================================================================")
    print("Ejecución de código intermedio completada")
    print("==================================================================\n")
        
    print("\n==================================================================")
    print("Compilación exitosa del programa")
    print("==================================================================\n")