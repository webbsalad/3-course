package main

import (
	"fmt"
	"sync"
	"time"
)

type BoundedSemaphore struct {
	tokens chan struct{}
	mu     sync.Mutex
	held   int
}

func NewBoundedSemaphore(max int) *BoundedSemaphore {
	return &BoundedSemaphore{
		tokens: make(chan struct{}, max),
	}
}

func (b *BoundedSemaphore) Acquire() {
	b.tokens <- struct{}{}
	b.mu.Lock()
	b.held++
	b.mu.Unlock()
}

func (b *BoundedSemaphore) Release() {
	b.mu.Lock()
	defer b.mu.Unlock()

	if b.held <= 0 {
		panic("semaphore release without acquire")
	}

	b.held--
	<-b.tokens

}

func worker(id int, sem *BoundedSemaphore, wg *sync.WaitGroup) {
	defer wg.Done()

	sem.Acquire()

	fmt.Printf("Worker %d started\n", id)
	time.Sleep(1 * time.Second) // Имитация работы
	fmt.Printf("Worker %d finished\n", id)

	sem.Release()

	if id%2 == 0 {
		fmt.Printf("Worker %d trying to release AGAIN (extra)\n", id)
		sem.Release()
	}
}

func main() {
	const (
		totalWorkers  = 10
		maxConcurrent = 2
	)

	sem := NewBoundedSemaphore(maxConcurrent)
	var wg sync.WaitGroup

	for i := 1; i <= totalWorkers; i++ {
		wg.Add(1)
		go worker(i, sem, &wg)
	}

	wg.Wait()
	fmt.Println("All workers completed")
}
