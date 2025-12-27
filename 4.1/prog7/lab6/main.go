package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"strings"
	"sync"
	"time"
)

type Task struct {
	ID          int       `json:"id"`
	Title       string    `json:"title"`
	Description string    `json:"description"`
	Status      string    `json:"status"`
	CreatedAt   time.Time `json:"createdAt"`
}

var (
	tasks  = make(map[int]Task)
	nextID = 1
	mu     sync.Mutex
)

func basicAuth(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		user, pass, ok := r.BasicAuth()
		if !ok || user != "admin" || pass != "admin123" {
			w.Header().Set("WWW-Authenticate", `Basic realm="Restricted"`)
			http.Error(w, "401 Unauthorized", http.StatusUnauthorized)
			return
		}
		next.ServeHTTP(w, r)
	}
}

func tasksHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	pathParts := strings.Split(strings.TrimPrefix(r.URL.Path, "/api/tasks"), "/")
	var id int
	if len(pathParts) > 1 && pathParts[1] != "" {
		id, _ = strconv.Atoi(pathParts[1])
	}

	switch r.Method {
	case "GET":
		if id != 0 {
			mu.Lock()
			task, ok := tasks[id]
			mu.Unlock()
			if !ok {
				http.Error(w, "Task not found", http.StatusNotFound)
				return
			}
			json.NewEncoder(w).Encode(task)
		} else {
			mu.Lock()
			taskList := make([]Task, 0, len(tasks))
			for _, t := range tasks {
				taskList = append(taskList, t)
			}
			mu.Unlock()
			json.NewEncoder(w).Encode(taskList)
		}

	case "POST":
		var t Task
		if err := json.NewDecoder(r.Body).Decode(&t); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		mu.Lock()
		t.ID = nextID
		nextID++
		t.CreatedAt = time.Now()
		tasks[t.ID] = t
		mu.Unlock()
		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(t)

	case "PUT":
		var updated Task
		if err := json.NewDecoder(r.Body).Decode(&updated); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		mu.Lock()
		task, ok := tasks[id]
		if ok {
			task.Title = updated.Title
			task.Description = updated.Description
			task.Status = updated.Status
			tasks[id] = task
			json.NewEncoder(w).Encode(task)
		} else {
			http.Error(w, "Task not found", http.StatusNotFound)
		}
		mu.Unlock()

	case "DELETE":
		mu.Lock()
		delete(tasks, id)
		mu.Unlock()
		w.WriteHeader(http.StatusNoContent)

	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
	}
}

func main() {
	http.HandleFunc("/api/tasks", basicAuth(tasksHandler))
	http.HandleFunc("/api/tasks/", basicAuth(tasksHandler))

	fmt.Println("Server starting at :8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
