package main

import (
	"io"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusOK)
		_, err := w.Write([]byte("приложение го работает"))
		if err != nil {
			log.Println("не удалось записать ответ:", err)
		}
	})

	http.HandleFunc("/echo", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			w.Header().Set("Allow", http.MethodPost)
			http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
			return
		}

		w.Header().Set("Content-Type", "application/octet-stream")
		if _, err := io.Copy(w, r.Body); err != nil {
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			log.Println("ошибка при копировании тела запроса:", err)
		}
	})

	if err := http.ListenAndServe(":8089", nil); err != nil {
		log.Fatalf("Ошибка запуска сервера: %v", err)
	}
}
