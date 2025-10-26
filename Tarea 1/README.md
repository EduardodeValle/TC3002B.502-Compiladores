# Tarea 1

Ejecutar el programa:
```bash
go run hello.go
```

---

La implementación del **stack**, **queue** y **dictionary** se realizó en el lenguaje **Go**, cada una con métodos de acceso y manipulación de datos. 

* **Stack**: implementación con `slices` nativos de Go, la complejidad temporal de inserción de datos y eliminación del último dato es de $O(1)$ en promedio.
* **Queue**: implementación mediante la librería estándar `container/list` debido a que la complejidad de eliminar el primer elemento de un slice es de $O(n)$, hay que recorrer a la izquierda todos los elementos del slice. Si bien la implementación del queue es mediante una lista doblemente enlazada, las operaciones de inserción de datos y eliminación del primer dato tienen una complejidad temporal de $O(1)$ en promedio.
* **Dictionary**: implementación con un `map` nativo de Go, la complejidad temporal de inserción, lectura y eliminación de datos es de $O(1)$ en promedio.