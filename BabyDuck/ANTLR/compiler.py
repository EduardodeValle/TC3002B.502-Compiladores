from antlr4 import *
import sys

from BabyDuckLexer import BabyDuckLexer
from BabyDuckParser import BabyDuckParser

from SemanticVisitor import SemanticVisitor
from VM import VirtualMachine

def run_compiler(filepath: str):
    """Pipeline completo de compilacion de BabyDuck"""
    print("Compilando ", filepath)
    input_stream = FileStream(filepath)
    lexer = BabyDuckLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = BabyDuckParser(stream)

    tree = parser.programa()
    visitor = SemanticVisitor()

    visitor.visit(tree)

    print("\n==================================================================")
    print("Semantica completada")
    print("==================================================================\n")

    print("\n==================================================================")
    print("Generacion de cuadruplos completada")
    print("==================================================================\n")

    obj_quadruples = visitor.quadruples
    obj_constants = visitor.get_constants_for_vm()

    vm = VirtualMachine(obj_quadruples, obj_constants)
    vm.execute()

    print("\n==================================================================")
    print("Ejecucion de codigo intermedio completada")
    print("==================================================================\n")

    print("\n==================================================================")
    print("Compilacion exitosa del programa")
    print("==================================================================\n")
