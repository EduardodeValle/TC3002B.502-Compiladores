# Suite de Pruebas Automatizadas - BabyDuck Compiler

## Estructura de Pruebas

```
ANTLR/
├── test_compiler.py      # Suite principal de pruebas pytest
├── run_tests.py          # Script para ejecutar todas las pruebas
├── pytest.ini            # Configuración de pytest
└── Tests/
    ├── ConSemantica/
    │   ├── Validos/      # 13 casos válidos que deben compilar
    │   └── Invalidos/    # 14 casos inválidos que deben fallar
    └── ErroresRuntime/   # 3 casos que fallan en tiempo de ejecución
```

## Ejecución de Pruebas

### Opción 1: Ejecutar Suite Completa (Recomendado)

```bash
python run_tests.py
```

Esto ejecuta automáticamente:
1. Todos los casos válidos (13 archivos)
2. Todos los casos inválidos (14 archivos)
3. Todos los errores de runtime (3 archivos)

Con separadores claros entre cada archivo y entre grupos.

### Opción 2: Ejecutar con pytest directamente

```bash
# Suite completa
pytest test_compiler.py -v -s

# Solo casos válidos
pytest test_compiler.py::TestBabyDuckCompiler::test_valid_programs -v -s

# Solo casos inválidos
pytest test_compiler.py::TestBabyDuckCompiler::test_invalid_programs -v -s

# Solo errores de runtime
pytest test_compiler.py::TestBabyDuckCompiler::test_runtime_errors -v -s

# Un archivo específico (usando tests individuales)
pytest test_compiler.py::TestIndividualValidCases -v -s -k "prueba1"
```

### Opción 3: Ejecutar archivo individual manualmente

```bash
python compiler.py "Tests/ConSemantica/Validos/prueba1.txt"
python compiler.py "Tests/ConSemantica/Invalidos/error_variable_no_declarada.txt"
python compiler.py "Tests/ErroresRuntime/error_division_cero.txt"
```

## Formato de Salida

### Casos Válidos
```
================================================================================
                        PRUEBAS DE CASOS VÁLIDOS
================================================================================

--------------------------------------------------------------------------------
 EJECUTANDO: prueba1.txt
--------------------------------------------------------------------------------
Compilando  Tests/ConSemantica/Validos/prueba1.txt
...
>>> EJECUCIÓN FINALIZADA CON ÉXITO <<<
...
 PASÓ: prueba1.txt
--------------------------------------------------------------------------------
```

### Casos Inválidos
```
================================================================================
                        PRUEBAS DE CASOS INVÁLIDOS
================================================================================

--------------------------------------------------------------------------------
 EJECUTANDO: error_variable_no_declarada.txt
--------------------------------------------------------------------------------
 PASÓ: error_variable_no_declarada.txt (detectó el error correctamente)

Error detectado:
ERROR EN SEMANTICO
La variable 'y' no declarada
Compilación abortada
--------------------------------------------------------------------------------
```

### Errores de Runtime
```
================================================================================
                   PRUEBAS DE ERRORES EN TIEMPO DE EJECUCIÓN
================================================================================

--------------------------------------------------------------------------------
 EJECUTANDO: error_division_cero.txt
--------------------------------------------------------------------------------
 PASÓ: error_division_cero.txt (error de runtime detectado)

Error detectado:
ERROR EN VM
Error de ejecucion: Division entre cero detectada
Compilación abortada
--------------------------------------------------------------------------------
```

## Clases de Prueba

### `TestBabyDuckCompiler`
Suite principal con tres tests:
- `test_valid_programs()`: Ejecuta todos los casos válidos
- `test_invalid_programs()`: Ejecuta todos los casos inválidos (errores semánticos)
- `test_runtime_errors()`: Ejecuta casos que generan errores en tiempo de ejecución

### `TestIndividualValidCases`
Tests parametrizados para ejecutar cada caso válido por separado.
Útil para debugging.

### `TestIndividualInvalidCases`
Tests parametrizados para ejecutar cada caso inválido por separado.
Útil para debugging.

## Resultados Esperados

### Casos Válidos (13)
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

### Casos Inválidos - Errores Semánticos (14)
Todos deben detectar error semántico:
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
Todos deben fallar durante la ejecución en la VM:
- **error_division_cero.txt**: División entre cero (10 / (5 - 5))
- **error_stack_overflow.txt**: Stack overflow por recursión infinita
- **error_variable_no_inicializada.txt**: Uso de variables no inicializadas (KeyError)

## Interpretación de Resultados

### Éxito Total
```
================================================================================
                        RESUMEN - CASOS VÁLIDOS
================================================================================
Total de archivos: 13
 Pasaron: 13
 Fallaron: 0

================================================================================
                        RESUMEN - CASOS INVÁLIDOS
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

Para debuggear un archivo específico:

```bash
# Ejecutar solo un test
pytest test_compiler.py -v -s -k "prueba1"

# Ver output detallado
python compiler.py "Tests/ConSemantica/Validos/prueba1.txt"
```

## Agregar Nuevas Pruebas

1. Crear archivo `.txt` en:
   - `Tests/ConSemantica/Validos/` - para casos válidos
   - `Tests/ConSemantica/Invalidos/` - para errores semánticos
   - `Tests/ErroresRuntime/` - para errores en tiempo de ejecución
2. Las pruebas se detectan automáticamente
3. Ejecutar `python run_tests.py`

No requiere modificar código de prueba.

## Diferencia entre Errores Semánticos y Errores de Runtime

### Errores Semánticos (Tests/ConSemantica/Invalidos/)
- Se detectan **durante la compilación** (análisis semántico)
- Ejemplos: variables no declaradas, tipos incompatibles, funciones duplicadas
- El programa **no llega a ejecutarse** en la VM

### Errores de Runtime (Tests/ErroresRuntime/)
- Se detectan **durante la ejecución** en la máquina virtual
- Ejemplos: división entre cero, stack overflow, variables no inicializadas
- El programa **pasa la fase de compilación** pero falla al ejecutarse
