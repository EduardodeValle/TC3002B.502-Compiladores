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

	fmt.Println("Inicial: ")
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

func main() {
	stack()

	fmt.Println("")

	queue()
}
