package main

import (
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

func main() {
	stack()
}
