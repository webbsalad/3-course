package main

import (
	"fmt"
	"sync"
	"time"
)

type SimpleSemaphore struct {
	tokens chan struct{}
}

func NewSimpleSemaphore(max int) *SimpleSemaphore {
	return &SimpleSemaphore{
		tokens: make(chan struct{}, max),
	}
}

func (s *SimpleSemaphore) Acquire() {
	s.tokens <- struct{}{}
}

func (s *SimpleSemaphore) Release() {
	<-s.tokens
}

func worker(id int, sem *SimpleSemaphore, wg *sync.WaitGroup) {
	defer wg.Done()

	sem.Acquire()
	fmt.Printf("Worker %d started\n", id)
	time.Sleep(1 * time.Second) // Имитация работы
	fmt.Printf("Worker %d finished\n", id)

	sem.Release()

	if id == 1 {
		fmt.Printf("Worker %d releasing (extra)\n", id)
		sem.Release()
	}
}

func main() {
	const (
		totalWorkers  = 10
		maxConcurrent = 2
	)

	sem := NewSimpleSemaphore(maxConcurrent)
	var wg sync.WaitGroup

	for i := 1; i <= totalWorkers; i++ {
		wg.Add(1)
		go worker(i, sem, &wg)
	}

	wg.Wait()
	fmt.Println("All workers completed")
}
