# Errores en Tiempo de Ejecución

Este directorio contiene archivos de prueba que provocan errores durante la ejecución en la máquina virtual, no durante el análisis semántico.

## Archivos de Prueba

### 1. error_division_cero.txt
**Error provocado:** `Division entre cero detectada`

Calcula una expresión que resulta en división entre cero: `10 / (5 - 5)`

**Salida esperada:**
```
Error de ejecucion: Division entre cero detectada
```

---

### 2. error_stack_overflow.txt
**Error provocado:** `Stack Overflow`

Función recursiva infinita que excede el límite de 1000 llamadas en el call stack.

**Salida esperada:**
```
Stack Overflow: Se excedió el límite de 1000 llamadas recursivas
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

## Cómo ejecutar estos tests

```bash
# Ejecutar individualmente
python compiler.py Tests/ErroresRuntime/error_division_cero.txt
python compiler.py Tests/ErroresRuntime/error_stack_overflow.txt
python compiler.py Tests/ErroresRuntime/error_variable_no_inicializada.txt
```

**Nota:** Estos archivos están diseñados para fallar en tiempo de ejecución, no durante la compilación.
