package main

import (
	"math/rand"
)

func sampleData(n int, scale int) []int {
	data := []int{} //empty dynamic array

	for x := 0; x < n; x++ {
		data = append(data, rand.Intn(scale))
	}

	return data
}
