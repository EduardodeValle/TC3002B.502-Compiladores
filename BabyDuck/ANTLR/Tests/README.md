# Tests de Análisis Semántico para BabyDuck

## Casos Válidos (Tests/ConSemantica/Validos)

### Básicos
1. **prueba1.txt** - Variables básicas, asignaciones, impresión
2. **prueba_expresiones.txt** - Expresiones aritméticas y booleanas completas
3. **if_while.txt** - Control de flujo básico (if/else, while)

### Funciones
4. **funcion_void.txt** - Funciones void con parámetros
5. **fibonacci_recursion.txt** - Recursión (Fibonacci)
6. **test_multiple_params.txt** - Funciones con múltiples parámetros (3+ parámetros)
7. **test_void_functions.txt** - Funciones void sin retorno explícito

### Características Avanzadas
8. **test_shadowing.txt** - Variables locales con mismo nombre que globales
9. **test_nested_calls.txt** - Llamadas a funciones anidadas como argumentos
10. **test_unary_operators.txt** - Operadores unarios (+ y -)
11. **test_nested_control.txt** - If y while anidados
12. **test_function_chain.txt** - Múltiples funciones llamándose entre sí
13. **test_complex_expressions.txt** - Expresiones con paréntesis muy anidados
14. **test_mixed_types.txt** - Operaciones con enteros y flotantes separados

### Resultados Esperados
Todos los archivos en Validos/ deben **compilar exitosamente** y ejecutarse sin errores.

---

## Casos Inválidos (Tests/ConSemantica/Invalidos)

### Errores de Variables
1. **error_variable_no_declarada.txt** - Uso de variable no declarada
2. **error_variable_duplicada.txt** - Declaración duplicada de variable en mismo scope

### Errores de Tipos
3. **error_tipo_incompatible.txt** - Asignación de flotante a entero
4. **error_operacion_invalida.txt** - Operación entre entero y flotante
5. **error_tipo_parametro.txt** - Argumento de tipo incorrecto en llamada

### Errores de Funciones
6. **error_funcion_no_declarada.txt** - Llamada a función no declarada
7. **error_funcion_duplicada.txt** - Declaración duplicada de función
8. **error_parametros_incorrectos.txt** - Cantidad incorrecta de parámetros
9. **error_sin_devolver.txt** - Función no-void sin devolver
10. **error_tipo_retorno.txt** - Devolver tipo incorrecto
11. **error_void_con_retorno.txt** - Función void con valor de retorno

### Errores de Control de Flujo
12. **error_condicion_no_booleana.txt** - Condición if con expresión no booleana
13. **error_while_no_booleano.txt** - Condición while con expresión no booleana

### Resultados Esperados
Todos los archivos en Invalidos/ deben **fallar con error semántico** apropiado.

---

## Cobertura de Características

### ✅ Tipos de Datos
- [x] Enteros
- [x] Flotantes
- [x] Booleanos (temporales)
- [x] Strings (solo en PRINT)

### ✅ Operadores
- [x] Aritméticos: +, -, *, /
- [x] Relacionales: >, <, ==, !=
- [x] Unarios: +, -

### ✅ Variables
- [x] Globales
- [x] Locales
- [x] Shadowing (local oculta global)
- [x] Inicialización

### ✅ Funciones
- [x] Con retorno (entero/flotante)
- [x] Void (sin retorno)
- [x] Con parámetros (1 a 3+)
- [x] Sin parámetros
- [x] Recursión
- [x] Llamadas anidadas

### ✅ Control de Flujo
- [x] If/else
- [x] While
- [x] Anidamiento

### ✅ Cuádruplos Generados
- [x] GOTO (inicial a main)
- [x] ERA, PARAMETER, GOSUB (llamadas)
- [x] RETURN (retornos)
- [x] GOTOF, GOTO (control flujo)
- [x] PRINT (salida)
- [x] Operaciones aritméticas
- [x] ENDFUNCTION, END

---

## Cómo Ejecutar

### Caso Válido
```bash
cd ANTLR
python main.py test_multiple_params.txt
```

### Caso Inválido
```bash
cd ANTLR
python main.py error_variable_no_declarada.txt
```

Debe mostrar error semántico apropiado.
