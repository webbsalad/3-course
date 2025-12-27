package main

import (
	"fmt"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

type Book struct {
	ID     int    `json:"id"`
	Title  string `json:"title" binding:"required,min=1,max=200"`
	Author string `json:"author" binding:"required,min=1,max=100"`
	Year   int    `json:"year" binding:"required,min=1000"`
	ISBN   string `json:"isbn" binding:"min=10,max=13"`
}

type BookUpdate struct {
	Title  *string `json:"title" binding:"omitempty,min=1,max=200"`
	Author *string `json:"author" binding:"omitempty,min=1,max=100"`
	Year   *int    `json:"year" binding:"omitempty,min=1000"`
	ISBN   *string `json:"isbn" binding:"omitempty,min=10,max=13"`
}

var booksDB = []Book{
	{ID: 1, Title: "Война и мир", Author: "Лев Толстой", Year: 1869, ISBN: "9785170987654"},
	{ID: 2, Title: "Преступление и наказание", Author: "Федор Достоевский", Year: 1866, ISBN: "9785170876543"},
	{ID: 3, Title: "Евгений Онегин", Author: "Александр Пушкин", Year: 1833, ISBN: "9785170765432"},
}

// @Summary Получить список всех книг
// @Tags Books
// @Produce json
// @Success 200 {array} Book
// @Router /books [get]
func getBooks(c *gin.Context) {
	author := c.Query("author")
	if author != "" {
		var filtered []Book
		for _, b := range booksDB {
			if b.Author == author {
				filtered = append(filtered, b)
			}
		}
		c.JSON(http.StatusOK, filtered)
		return
	}
	c.JSON(http.StatusOK, booksDB)
}

// @Summary Получить книгу по ID
// @Tags Books
// @Produce json
// @Param id path int true "Book ID"
// @Success 200 {object} Book
// @Failure 404 {object} map[string]string
// @Router /books/{id} [get]
func getBook(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
		return
	}

	for _, book := range booksDB {
		if book.ID == id {
			c.JSON(http.StatusOK, book)
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"detail": fmt.Sprintf("Книга с ID %d не найдена", id)})
}

// @Summary Создать новую книгу
// @Tags Books
// @Accept json
// @Produce json
// @Param book body Book true "Данные книги"
// @Success 201 {object} Book
// @Failure 400 {object} map[string]string
// @Router /books [post]
func createBook(c *gin.Context) {
	var newBook Book

	if err := c.ShouldBindJSON(&newBook); err != nil {
		c.JSON(http.StatusUnprocessableEntity, gin.H{"error": err.Error()})
		return
	}

	if newBook.Year > time.Now().Year() {
		c.JSON(http.StatusUnprocessableEntity, gin.H{"error": "Year cannot be in the future"})
		return
	}

	newBook.ID = nextID
	nextID++
	booksDB = append(booksDB, newBook)

	c.JSON(http.StatusCreated, newBook)
}

// @Summary Полное обновление книги
// @Tags Books
// @Accept json
// @Produce json
// @Param id path int true "Book ID"
// @Param book body Book true "Новые данные"
// @Success 200 {object} Book
// @Failure 404 {object} map[string]string
// @Router /books/{id} [put]
func updateBook(c *gin.Context) {
	id, _ := strconv.Atoi(c.Param("id"))
	var updatedData Book

	if err := c.ShouldBindJSON(&updatedData); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	for i, book := range booksDB {
		if book.ID == id {
			updatedData.ID = id
			booksDB[i] = updatedData
			c.JSON(http.StatusOK, updatedData)
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"detail": "Book not found"})
}

// @Summary Частичное обновление книги
// @Tags Books
// @Accept json
// @Produce json
// @Param id path int true "Book ID"
// @Param book body BookUpdate true "Поля для обновления"
// @Success 200 {object} Book
// @Router /books/{id} [patch]
func partialUpdateBook(c *gin.Context) {
	id, _ := strconv.Atoi(c.Param("id"))
	var updateData BookUpdate

	if err := c.ShouldBindJSON(&updateData); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	for i, book := range booksDB {
		if book.ID == id {
			if updateData.Title != nil {
				booksDB[i].Title = *updateData.Title
			}
			if updateData.Author != nil {
				booksDB[i].Author = *updateData.Author
			}
			if updateData.Year != nil {
				booksDB[i].Year = *updateData.Year
			}
			if updateData.ISBN != nil {
				booksDB[i].ISBN = *updateData.ISBN
			}
			c.JSON(http.StatusOK, booksDB[i])
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"detail": "Book not found"})
}

// @Summary Удалить книгу
// @Tags Books
// @Param id path int true "Book ID"
// @Success 204
// @Router /books/{id} [delete]
func deleteBook(c *gin.Context) {
	id, _ := strconv.Atoi(c.Param("id"))

	for i, book := range booksDB {
		if book.ID == id {
			booksDB = append(booksDB[:i], booksDB[i+1:]...)
			c.Status(http.StatusNoContent)
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"detail": "Book not found"})
}

var nextID = 4

// @title Books API
// @version 1.0
// @description REST API для управления библиотекой книг (Go implementation)
// @host localhost:8080
// @BasePath /api
func main() {
	r := gin.Default()

	r.GET("/docs/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	api := r.Group("/api")
	{
		api.GET("/books", getBooks)
		api.GET("/books/:id", getBook)
		api.POST("/books", createBook)
		api.PUT("/books/:id", updateBook)
		api.PATCH("/books/:id", partialUpdateBook)
		api.DELETE("/books/:id", deleteBook)
	}

	r.Run(":8080")
}
