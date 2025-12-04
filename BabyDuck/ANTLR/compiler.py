from antlr4 import *
import sys

from BabyDuckLexer import BabyDuckLexer
from BabyDuckParser import BabyDuckParser

from SemanticVisitor import SemanticVisitor
from VM import VirtualMachine

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
    visitor = SemanticVisitor()

    visitor.visit(tree)
    
    print("\n==================================================================")
    print("Semántica completada")
    print("==================================================================\n")

    print("\n==================================================================")
    print("Generación de cuádruplos completada")
    print("==================================================================\n")

    # extraer artefactos del compilador
    obj_quadruples = visitor.quadruples
    obj_dir_func = visitor.dir_func
    obj_constants = visitor.get_constants_for_vm()

    vm = VirtualMachine(obj_quadruples, obj_constants, obj_dir_func)
    vm.execute()

    print("\n==================================================================")
    print("Ejecución de código intermedio completada")
    print("==================================================================\n")
        
    print("\n==================================================================")
    print("Compilación exitosa del programa")
    print("==================================================================\n")