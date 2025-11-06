import sys
from BabyDuckError import BabyDuckError 
from compiler import run_compiler

def main():
    if len(sys.argv) < 2:
        print("Error: no se ingresó un archivo para compilar")
        print("Uso: python main.py file.BabyDuck")
        sys.exit(1)
        
    filepath = sys.argv[1]

    try:
        run_compiler(filepath)
        
    except BabyDuckError as e:
        # Error encontrado en semántica, generación de cuádruplos o máquina virtual        
        print("\n\nCompilación fallida", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)
    
    except Exception as e:
        print("Error inesperado del compilador: ", e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()