package main

import (
	"fmt"
	"sync"
	"time"

	"github.com/google/uuid"
)

type token struct {
	id string
}

type BoundedSemaphore struct {
	tokens chan token
	mu     sync.Mutex
	held   map[string]struct{}
}

func NewBoundedSemaphore(max int) *BoundedSemaphore {
	return &BoundedSemaphore{
		tokens: make(chan token, max),
		held:   make(map[string]struct{}),
	}
}

func (b *BoundedSemaphore) Acquire() token {
	t := token{id: uuid.New().String()}
	b.tokens <- t

	b.mu.Lock()
	b.held[t.id] = struct{}{}
	b.mu.Unlock()

	return t
}

func (b *BoundedSemaphore) Release(t token) {
	b.mu.Lock()
	defer b.mu.Unlock()

	if _, ok := b.held[t.id]; !ok {
		panic("semaphore release without valid acquire")
	}

	delete(b.held, t.id)

	select {
	case <-b.tokens:
	default:
		panic("inconsistent state: no token to release")
	}
}

func worker(id int, sem *BoundedSemaphore, wg *sync.WaitGroup) {
	defer wg.Done()

	t := sem.Acquire()

	fmt.Printf("Worker %d started\n", id)
	time.Sleep(1 * time.Second) // Имитация работы
	fmt.Printf("Worker %d finished\n", id)

	sem.Release(t)

}

func main() {
	const (
		totalWorkers  = 10000
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
