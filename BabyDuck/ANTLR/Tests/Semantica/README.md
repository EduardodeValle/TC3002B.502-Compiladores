# Tests de Analisis Semantico para BabyDuck

## Casos Validos (Tests/Semantica/Validos)

### Basicos
1. **prueba1.txt** - Variables basicas, asignaciones, impresion
2. **prueba_expresiones.txt** - Expresiones aritmeticas y booleanas completas
3. **if_while.txt** - Control de flujo basico (if/else, while)

### Funciones
4. **funcion_void.txt** - Funciones void con parametros
5. **fibonacci_recursion.txt** - Recursion (Fibonacci)
6. **test_multiple_params.txt** - Funciones con multiples parametros (3+ parametros)
7. **test_void_functions.txt** - Funciones void sin retorno explicito

### Caracteristicas Avanzadas
8. **test_shadowing.txt** - Variables locales con mismo nombre que globales
9. **test_nested_calls.txt** - Llamadas a funciones anidadas como argumentos
10. **test_unary_operators.txt** - Operadores unarios (+ y -)
11. **test_nested_control.txt** - If y while anidados
12. **test_function_chain.txt** - Multiples funciones llamandose entre si
13. **test_complex_expressions.txt** - Expresiones con parentesis muy anidados
14. **test_mixed_types.txt** - Operaciones con enteros y flotantes separados

### Resultados Esperados
Todos los archivos en Validos/ deben **compilar exitosamente** y ejecutarse sin errores.

---

## Casos Invalidos (Tests/Semantica/Invalidos)

### Errores de Variables
1. **error_variable_no_declarada.txt** - Uso de variable no declarada
2. **error_variable_duplicada.txt** - Declaracion duplicada de variable en mismo scope

### Errores de Tipos
3. **error_tipo_incompatible.txt** - Asignacion de flotante a entero
4. **error_operacion_invalida.txt** - Operacion entre entero y flotante
5. **error_tipo_parametro.txt** - Argumento de tipo incorrecto en llamada

### Errores de Funciones
6. **error_funcion_no_declarada.txt** - Llamada a funcion no declarada
7. **error_funcion_duplicada.txt** - Declaracion duplicada de funcion
8. **error_parametros_incorrectos.txt** - Cantidad incorrecta de parametros
9. **error_sin_devolver.txt** - Funcion no-void sin devolver
10. **error_tipo_retorno.txt** - Devolver tipo incorrecto
11. **error_void_con_retorno.txt** - Funcion void con valor de retorno

### Errores de Control de Flujo
12. **error_condicion_no_booleana.txt** - Condicion if con expresion no booleana
13. **error_while_no_booleano.txt** - Condicion while con expresion no booleana

### Resultados Esperados
Todos los archivos en Invalidos/ deben **fallar con error semantico** apropiado.

---

## Cobertura de Caracteristicas

### ✅ Tipos de Datos
- [x] Enteros
- [x] Flotantes
- [x] Booleanos (temporales)
- [x] Strings (solo en PRINT)

### ✅ Operadores
- [x] Aritmeticos: +, -, *, /
- [x] Relacionales: >, <, ==, !=
- [x] Unarios: +, -

### ✅ Variables
- [x] Globales
- [x] Locales
- [x] Shadowing (local oculta global)
- [x] Inicializacion

### ✅ Funciones
- [x] Con retorno (entero/flotante)
- [x] Void (sin retorno)
- [x] Con parametros (1 a 3+)
- [x] Sin parametros
- [x] Recursion
- [x] Llamadas anidadas

### ✅ Control de Flujo
- [x] If/else
- [x] While
- [x] Anidamiento

### ✅ Cuadruplos Generados
- [x] GOTO (inicial a main)
- [x] ERA, PARAMETER, GOSUB (llamadas)
- [x] RETURN (retornos)
- [x] GOTOF, GOTO (control flujo)
- [x] PRINT (salida)
- [x] Operaciones aritmeticas
- [x] ENDFUNCTION, END

---

## Como Ejecutar

### Caso Valido
```bash
cd ANTLR
python main.py test_multiple_params.txt
```

### Caso Invalido
```bash
cd ANTLR
python main.py error_variable_no_declarada.txt
```

Debe mostrar error semantico apropiado.
