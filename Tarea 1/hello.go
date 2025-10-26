package main

import (
	"container/list"
	"fmt"
)

func stack() {
	stack := []int{}
	fmt.Println("Inicial:", stack)

	stack = append(stack, 10)
	fmt.Println("Push 10:", stack)

	stack = append(stack, 20)
	fmt.Println("Push 20:", stack)

	stack = append(stack, 30)
	fmt.Println("Push 30:", stack)

	topElement := stack[len(stack)-1]
	fmt.Println("Peek:", topElement)
	
	fmt.Println("Stack actual:", stack)

	stack = stack[:len(stack)-1]
	fmt.Println("Pop:", stack)

	stack = stack[:len(stack)-1]
	fmt.Println("Pop:", stack)
}

// No se puede imprimir el contenido de la queue
// directamente con fmt.Println(queue) porque no
// imprime el contenido, imprime un puntero
func printQueue(queue *list.List) {
	for e := queue.Front(); e != nil; e = e.Next() {
		fmt.Printf("%v ", e.Value)
	}
	fmt.Println()
}

func queue() {
	queue := list.New()

	fmt.Print("Inicial: ")
	printQueue(queue)

	queue.PushBack(10)
	fmt.Println("Enqueue 10: ")
	printQueue(queue)

	queue.PushBack(20)
	fmt.Println("Enqueue 20: ")
	printQueue(queue)

	queue.PushBack(30)
	fmt.Println("Enqueue 30: ")
	printQueue(queue)

	frontElement := queue.Front()
	fmt.Println("Peek:", frontElement.Value)

	fmt.Println("Queue actual: ")
	printQueue(queue)

	queue.Remove(queue.Front())
	fmt.Println("Dequeue: ")
	printQueue(queue)
	
	queue.Remove(queue.Front())
	fmt.Println("Dequeue: ")
}

func hashmap() {
	puertosServicio := make(map[string]int)

	fmt.Println("Mapa de puertos inicial:", puertosServicio)

	puertosServicio["http"] = 80
	fmt.Println("Asignando puerto 'http':", puertosServicio)

	puertosServicio["https"] = 443
	fmt.Println("Asignando puerto 'https':", puertosServicio)

	puertosServicio["ssh"] = 22
	fmt.Println("Asignando puerto 'ssh':", puertosServicio)

	puertoSsh := puertosServicio["ssh"]
	fmt.Println("Consultando puerto 'ssh':", puertoSsh)

	puerto, existe := puertosServicio["https"]
	if existe {
		fmt.Println("Consultando 'https' (sí existe):", puerto)
	}

	_, existe = puertosServicio["ftp"]
	if !existe {
		fmt.Println("Consultando 'ftp' (no existe):", "El servicio no está registrado")
	}

	delete(puertosServicio, "ssh")
	fmt.Println("Eliminando servicio 'ssh':", puertosServicio)

	delete(puertosServicio, "http")
	fmt.Println("Eliminando servicio 'http':", puertosServicio)
}

func main() {
	stack()

	fmt.Println("")

	queue()

	fmt.Println("")

	hashmap()
}
