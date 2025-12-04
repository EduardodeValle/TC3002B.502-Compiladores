# Errores en Tiempo de Ejecucion

Este directorio contiene archivos de prueba que provocan errores durante la ejecucion en la maquina virtual, no durante el analisis semantico.

## Archivos de Prueba

### 1. error_division_cero.txt
**Error provocado:** `Division entre cero detectada`

Calcula una expresion que resulta en division entre cero: `10 / (5 - 5)`

**Salida esperada:**
```
Error de ejecucion: Division entre cero detectada
```

---

### 2. error_stack_overflow.txt
**Error provocado:** `Stack Overflow`

Funcion recursiva infinita que excede el limite de 1000 llamadas en el call stack.

**Salida esperada:**
```
Stack Overflow: Se excedio el limite de 1000 llamadas recursivas
```

---

### 3. error_variable_no_inicializada.txt
**Error provocado:** `KeyError` al intentar leer variable no inicializada

Intenta usar variables que fueron declaradas pero nunca inicializadas.

**Salida esperada:**
```
KeyError: <address>
```

---

## Como ejecutar estos tests

```bash
# Ejecutar individualmente
python compiler.py Tests/ErroresRuntime/error_division_cero.txt
python compiler.py Tests/ErroresRuntime/error_stack_overflow.txt
python compiler.py Tests/ErroresRuntime/error_variable_no_inicializada.txt
```

**Nota:** Estos archivos estan diseñados para fallar en tiempo de ejecucion, no durante la compilacion.
