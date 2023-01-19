package main

import "fmt"

func sum(s []int, c chan int) {
	sum := 0
	for _, v := range s {
		sum += v
	}
	c <- sum
	fmt.Printf("send %v to chan // ", sum)
}

func gort() {
	s := []int{1, 2, 3, 4, 5, 6, 7}

	c := make(chan int)
	go sum(s[:len(s)/2], c)
	go sum(s[len(s)/2:], c)

	x := <-c
	fmt.Printf("receive %v from chan // ", x)
	y := <-c
	fmt.Printf("receive %v from chan // ", y)

	fmt.Println(x, y)
}
