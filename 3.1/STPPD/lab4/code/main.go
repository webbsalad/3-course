// Package main демонстрирует использование GoFiber с JWT для сохранения и увеличения версии.
// Сервер генерирует JWT, который содержит текущую "версию". При каждом запросе версия увеличивается,
// и токен обновляется, возвращаясь клиенту.
package main

import (
	"log"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/golang-jwt/jwt/v4"
)

// SecretKey используется для подписи JWT.
// Это ключ, который должен оставаться в секрете для предотвращения подделки токенов.
var SecretKey = []byte("supersecretkey")

// GenerateToken создает новый JWT с указанной версией.
//
// Аргументы:
// - version (int): текущая версия, которая будет сохранена в токене.
//
// Возвращает:
// - string: сгенерированный JWT.
// - error: ошибка, если токен не удалось создать.
func GenerateToken(version int) (string, error) {
	claims := jwt.MapClaims{
		"version": version,
		"exp":     time.Now().Add(time.Hour * 1).Unix(), // Токен истекает через 1 час
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(SecretKey)
}

// ParseToken разбирает JWT и извлекает из него версию.
//
// Аргументы:
// - tokenString (string): строка JWT, переданная клиентом.
//
// Возвращает:
// - int: извлеченная версия.
// - error: ошибка, если токен недействителен или произошла ошибка при разборе.
func ParseToken(tokenString string) (int, error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		return SecretKey, nil
	})
	if err != nil {
		return 0, err
	}
	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		if version, ok := claims["version"].(float64); ok {
			return int(version), nil
		}
	}
	return 0, fiber.ErrUnauthorized
}

// main — это точка входа приложения. Оно запускает HTTP-сервер,
// который обрабатывает запросы с использованием JWT.
//
// Сервер работает на порту 3000.
func main() {
	// Создаем приложение Fiber.
	app := fiber.New()

	// Добавляем middleware для логирования запросов.
	app.Use(logger.New())

	// Основной маршрут с JWT логикой.
	// Он считывает токен из куки, увеличивает версию, генерирует новый токен
	// и возвращает текущую версию клиенту.
	app.Get("/", func(c *fiber.Ctx) error {
		// Считываем JWT из заголовка
		tokenString := c.Cookies("jwt")

		var version int
		var err error

		// Если JWT существует, парсим его.
		if tokenString != "" {
			version, err = ParseToken(tokenString)
			if err != nil {
				// Если ошибка парсинга, возвращаем 401
				return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{
					"error": "Неверный токен",
				})
			}
		} else {
			// Если токена нет, начинаем с версии 0
			version = 0
		}

		// Увеличиваем версию
		version++

		// Генерируем новый токен с обновленной версией.
		newToken, err := GenerateToken(version)
		if err != nil {
			return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
				"error": "Ошибка генерации токена",
			})
		}

		// Устанавливаем новый токен в куки.
		c.Cookie(&fiber.Cookie{
			Name:     "jwt",
			Value:    newToken,
			HTTPOnly: true,
			Expires:  time.Now().Add(time.Hour * 1), // Токен живет 1 час
		})

		// Возвращаем текущую версию.
		return c.JSON(fiber.Map{
			"version": version,
		})
	})

	// Запускаем сервер.
	log.Println("Сервер запущен на http://localhost:3000")
	log.Fatal(app.Listen(":3000"))
}
