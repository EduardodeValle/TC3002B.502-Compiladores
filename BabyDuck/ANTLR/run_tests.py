#!/usr/bin/env python3
"""
Script para ejecutar las pruebas del compilador BabyDuck con formato mejorado
"""

import sys
import pytest

def main():
    """Ejecuta las pruebas con configuración personalizada"""

    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                   SUITE DE PRUEBAS - COMPILADOR BABYDUCK                   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

    # Configuración de pytest
    args = [
        "test_compiler.py",
        "-v",                    # Verbose
        "-s",                    # No capturar output
        "--tb=short",            # Traceback corto
        "--color=yes",           # Colores
        "-k", "test_valid_programs or test_invalid_programs",  # Solo los tests principales
    ]

    # Ejecutar pytest
    exit_code = pytest.main(args)

    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                         FIN DE LAS PRUEBAS                                 ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
