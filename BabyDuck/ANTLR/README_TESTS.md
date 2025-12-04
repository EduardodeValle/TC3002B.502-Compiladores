# Suite de Pruebas Automatizadas - BabyDuck Compiler

## Estructura de Pruebas

```
ANTLR/
├── test_compiler.py      # Suite principal de pruebas pytest
├── run_tests.py          # Script para ejecutar todas las pruebas
├── pytest.ini            # Configuración de pytest
└── Tests/
    └── ConSemantica/
        ├── Validos/      # 14 casos válidos que deben compilar
        └── Invalidos/    # 13 casos inválidos que deben fallar
```

## Ejecución de Pruebas

### Opción 1: Ejecutar Suite Completa (Recomendado)

```bash
python run_tests.py
```

Esto ejecuta automáticamente:
1. ✅ Todos los casos válidos (14 archivos)
2. ❌ Todos los casos inválidos (13 archivos)

Con separadores claros entre cada archivo y entre grupos.

### Opción 2: Ejecutar con pytest directamente

```bash
# Suite completa
pytest test_compiler.py -v -s

# Solo casos válidos
pytest test_compiler.py::TestBabyDuckCompiler::test_valid_programs -v -s

# Solo casos inválidos
pytest test_compiler.py::TestBabyDuckCompiler::test_invalid_programs -v -s

# Un archivo específico (usando tests individuales)
pytest test_compiler.py::TestIndividualValidCases -v -s -k "prueba1"
```

### Opción 3: Ejecutar archivo individual manualmente

```bash
python main.py "Tests/ConSemantica/Validos/prueba1.txt"
python main.py "Tests/ConSemantica/Invalidos/error_variable_no_declarada.txt"
```

## Formato de Salida

### Casos Válidos
```
================================================================================
                        PRUEBAS DE CASOS VÁLIDOS
================================================================================

--------------------------------------------------------------------------------
📝 EJECUTANDO: prueba1.txt
--------------------------------------------------------------------------------
Compilando  Tests/ConSemantica/Validos/prueba1.txt
...
>>> EJECUCIÓN FINALIZADA CON ÉXITO <<<
...
✅ PASÓ: prueba1.txt
--------------------------------------------------------------------------------
```

### Casos Inválidos
```
================================================================================
                        PRUEBAS DE CASOS INVÁLIDOS
================================================================================

--------------------------------------------------------------------------------
📝 EJECUTANDO: error_variable_no_declarada.txt
--------------------------------------------------------------------------------
✅ PASÓ: error_variable_no_declarada.txt (detectó el error correctamente)

Error detectado:
ERROR EN SEMANTICO
La variable 'y' no declarada
Compilación abortada
--------------------------------------------------------------------------------
```

## Clases de Prueba

### `TestBabyDuckCompiler`
Suite principal con dos tests:
- `test_valid_programs()`: Ejecuta todos los casos válidos
- `test_invalid_programs()`: Ejecuta todos los casos inválidos

### `TestIndividualValidCases`
Tests parametrizados para ejecutar cada caso válido por separado.
Útil para debugging.

### `TestIndividualInvalidCases`
Tests parametrizados para ejecutar cada caso inválido por separado.
Útil para debugging.

## Resultados Esperados

### Casos Válidos (14)
Todos deben compilar y ejecutar exitosamente:
- ✅ prueba1.txt
- ✅ prueba_expresiones.txt
- ✅ if_while.txt
- ✅ funcion_void.txt
- ✅ fibonacci_recursion.txt
- ✅ test_multiple_params.txt
- ✅ test_shadowing.txt
- ✅ test_nested_calls.txt
- ✅ test_unary_operators.txt
- ✅ test_nested_control.txt
- ✅ test_function_chain.txt
- ✅ test_complex_expressions.txt
- ✅ test_void_functions.txt
- ✅ test_mixed_types.txt

### Casos Inválidos (13)
Todos deben detectar error semántico:
- ❌ error_variable_no_declarada.txt
- ❌ error_variable_duplicada.txt
- ❌ error_tipo_incompatible.txt
- ❌ error_operacion_invalida.txt
- ❌ error_funcion_no_declarada.txt
- ❌ error_funcion_duplicada.txt
- ❌ error_parametros_incorrectos.txt
- ❌ error_tipo_parametro.txt
- ❌ error_sin_devolver.txt
- ❌ error_tipo_retorno.txt
- ❌ error_void_con_retorno.txt
- ❌ error_condicion_no_booleana.txt
- ❌ error_while_no_booleano.txt

## Interpretación de Resultados

### Éxito Total
```
================================================================================
                        RESUMEN - CASOS VÁLIDOS
================================================================================
Total de archivos: 14
✅ Pasaron: 14
❌ Fallaron: 0

================================================================================
                        RESUMEN - CASOS INVÁLIDOS
================================================================================
Total de archivos: 13
✅ Pasaron (detectaron error): 13
❌ Fallaron (no detectaron error): 0
```

### Si hay fallos
Los archivos que fallan aparecen listados en el resumen final con detalles del error.

## Debugging Individual

Para debuggear un archivo específico:

```bash
# Ejecutar solo un test
pytest test_compiler.py -v -s -k "prueba1"

# Ver output detallado
python main.py "Tests/ConSemantica/Validos/prueba1.txt"
```

## Agregar Nuevas Pruebas

1. Crear archivo `.txt` en `Tests/ConSemantica/Validos/` o `Invalidos/`
2. Las pruebas se detectan automáticamente
3. Ejecutar `python run_tests.py`

No requiere modificar código de prueba.
