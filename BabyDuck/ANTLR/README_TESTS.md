# Suite de Pruebas Automatizadas - BabyDuck Compiler

## Estructura de Pruebas

```
ANTLR/
├── test_compiler.py      # Suite principal de pruebas pytest
├── run_tests.py          # Script para ejecutar todas las pruebas
├── pytest.ini            # Configuracion de pytest
└── Tests/
    ├── ConSemantica/
    │   ├── Validos/      # 13 casos validos que deben compilar
    │   └── Invalidos/    # 14 casos invalidos que deben fallar
    └── ErroresRuntime/   # 3 casos que fallan en tiempo de ejecucion
```

## Ejecucion de Pruebas

### Opcion 1: Ejecutar Suite Completa (Recomendado)

```bash
python run_tests.py
```

Esto ejecuta automaticamente:
1. Todos los casos validos (13 archivos)
2. Todos los casos invalidos (14 archivos)
3. Todos los errores de runtime (3 archivos)

Con separadores claros entre cada archivo y entre grupos.

### Opcion 2: Ejecutar con pytest directamente

```bash
# Suite completa
pytest test_compiler.py -v -s

# Solo casos validos
pytest test_compiler.py::TestBabyDuckCompiler::test_valid_programs -v -s

# Solo casos invalidos
pytest test_compiler.py::TestBabyDuckCompiler::test_invalid_programs -v -s

# Solo errores de runtime
pytest test_compiler.py::TestBabyDuckCompiler::test_runtime_errors -v -s

# Un archivo especifico (usando tests individuales)
pytest test_compiler.py::TestIndividualValidCases -v -s -k "prueba1"
```

### Opcion 3: Ejecutar archivo individual manualmente

```bash
python compiler.py "Tests/ConSemantica/Validos/prueba1.txt"
python compiler.py "Tests/ConSemantica/Invalidos/error_variable_no_declarada.txt"
python compiler.py "Tests/ErroresRuntime/error_division_cero.txt"
```

## Formato de Salida

### Casos Validos
```
================================================================================
                        PRUEBAS DE CASOS VALIDOS
================================================================================

--------------------------------------------------------------------------------
 EJECUTANDO: prueba1.txt
--------------------------------------------------------------------------------
Compilando  Tests/ConSemantica/Validos/prueba1.txt
...
>>> EJECUCION FINALIZADA CON EXITO <<<
...
 PASO: prueba1.txt
--------------------------------------------------------------------------------
```

### Casos Invalidos
```
================================================================================
                        PRUEBAS DE CASOS INVALIDOS
================================================================================

--------------------------------------------------------------------------------
 EJECUTANDO: error_variable_no_declarada.txt
--------------------------------------------------------------------------------
 PASO: error_variable_no_declarada.txt (detecto el error correctamente)

Error detectado:
ERROR EN SEMANTICO
La variable 'y' no declarada
Compilacion abortada
--------------------------------------------------------------------------------
```

### Errores de Runtime
```
================================================================================
                   PRUEBAS DE ERRORES EN TIEMPO DE EJECUCION
================================================================================

--------------------------------------------------------------------------------
 EJECUTANDO: error_division_cero.txt
--------------------------------------------------------------------------------
 PASO: error_division_cero.txt (error de runtime detectado)

Error detectado:
ERROR EN VM
Error de ejecucion: Division entre cero detectada
Compilacion abortada
--------------------------------------------------------------------------------
```

## Clases de Prueba

### `TestBabyDuckCompiler`
Suite principal con tres tests:
- `test_valid_programs()`: Ejecuta todos los casos validos
- `test_invalid_programs()`: Ejecuta todos los casos invalidos (errores semanticos)
- `test_runtime_errors()`: Ejecuta casos que generan errores en tiempo de ejecucion

### `TestIndividualValidCases`
Tests parametrizados para ejecutar cada caso valido por separado.
Util para debugging.

### `TestIndividualInvalidCases`
Tests parametrizados para ejecutar cada caso invalido por separado.
Util para debugging.

## Resultados Esperados

### Casos Validos (13)
Todos deben compilar y ejecutar exitosamente:
- prueba1.txt
- prueba_expresiones.txt
- if_while.txt
- funcion_void.txt
- fibonacci_recursion.txt
- test_multiple_params.txt
- test_shadowing.txt
- test_nested_calls.txt
- test_unary_operators.txt
- test_nested_control.txt
- test_function_chain.txt
- test_void_functions.txt
- test_mixed_types.txt

### Casos Invalidos - Errores Semanticos (14)
Todos deben detectar error semantico:
- error_variable_no_declarada.txt
- error_variable_duplicada.txt
- error_tipo_incompatible.txt
- error_operacion_invalida.txt
- error_funcion_no_declarada.txt
- error_funcion_duplicada.txt
- error_parametros_incorrectos.txt
- error_tipo_parametro.txt
- error_sin_devolver.txt
- error_tipo_retorno.txt
- error_void_con_retorno.txt
- error_condicion_no_booleana.txt
- error_while_no_booleano.txt
- test_complex_expressions.txt

### Errores de Runtime (3)
Todos deben fallar durante la ejecucion en la VM:
- **error_division_cero.txt**: Division entre cero (10 / (5 - 5))
- **error_stack_overflow.txt**: Stack overflow por recursion infinita
- **error_variable_no_inicializada.txt**: Uso de variables no inicializadas (KeyError)

## Interpretacion de Resultados

### Exito Total
```
================================================================================
                        RESUMEN - CASOS VALIDOS
================================================================================
Total de archivos: 13
 Pasaron: 13
 Fallaron: 0

================================================================================
                        RESUMEN - CASOS INVALIDOS
================================================================================
Total de archivos: 14
 Pasaron (detectaron error): 14
 Fallaron (no detectaron error): 0

================================================================================
                        RESUMEN - ERRORES DE RUNTIME
================================================================================
Total de archivos: 3
 Pasaron (error detectado): 3
 Fallaron (error no detectado): 0
```

### Si hay fallos
Los archivos que fallan aparecen listados en el resumen final con detalles del error.

## Debugging Individual

Para debuggear un archivo especifico:

```bash
# Ejecutar solo un test
pytest test_compiler.py -v -s -k "prueba1"

# Ver output detallado
python compiler.py "Tests/ConSemantica/Validos/prueba1.txt"
```

## Agregar Nuevas Pruebas

1. Crear archivo `.txt` en:
   - `Tests/ConSemantica/Validos/` - para casos validos
   - `Tests/ConSemantica/Invalidos/` - para errores semanticos
   - `Tests/ErroresRuntime/` - para errores en tiempo de ejecucion
2. Las pruebas se detectan automaticamente
3. Ejecutar `python run_tests.py`

No requiere modificar codigo de prueba.

## Diferencia entre Errores Semanticos y Errores de Runtime

### Errores Semanticos (Tests/ConSemantica/Invalidos/)
- Se detectan **durante la compilacion** (analisis semantico)
- Ejemplos: variables no declaradas, tipos incompatibles, funciones duplicadas
- El programa **no llega a ejecutarse** en la VM

### Errores de Runtime (Tests/ErroresRuntime/)
- Se detectan **durante la ejecucion** en la maquina virtual
- Ejemplos: division entre cero, stack overflow, variables no inicializadas
- El programa **pasa la fase de compilacion** pero falla al ejecutarse
