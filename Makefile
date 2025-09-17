.PHONY: build run clean install deps help

# Переменные
BINARY_NAME=fan
MAIN_FILE=main.go

# Цвета для вывода
GREEN=\033[0;32m
YELLOW=\033[1;33m
RED=\033[0;31m
NC=\033[0m # No Color

help: ## Показать справку
	@echo "$(GREEN)Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

deps: ## Установить зависимости
	@echo "$(GREEN)Устанавливаем зависимости...$(NC)"
	go mod tidy
	go mod download

build: deps ## Собрать приложение
	@echo "$(GREEN)Собираем приложение...$(NC)"
	go build -o $(BINARY_NAME) $(MAIN_FILE)
	@echo "$(GREEN)Сборка завершена! Исполняемый файл: $(BINARY_NAME)$(NC)"

run: build ## Запустить приложение
	@echo "$(GREEN)Запускаем приложение...$(NC)"
	./$(BINARY_NAME)

install: build ## Установить приложение в систему
	@echo "$(GREEN)Устанавливаем приложение...$(NC)"
	sudo cp $(BINARY_NAME) /usr/local/bin/
	@echo "$(GREEN)Приложение установлено! Теперь можно использовать команду 'fan'$(NC)"

clean: ## Очистить собранные файлы
	@echo "$(GREEN)Очищаем...$(NC)"
	rm -f $(BINARY_NAME)
	@echo "$(GREEN)Очистка завершена!$(NC)"

test: ## Запустить тесты
	@echo "$(GREEN)Запускаем тесты...$(NC)"
	go test ./...

fmt: ## Форматировать код
	@echo "$(GREEN)Форматируем код...$(NC)"
	go fmt ./...

lint: ## Проверить код линтером
	@echo "$(GREEN)Проверяем код...$(NC)"
	golangci-lint run

# Примеры использования
demo: build ## Показать демо использования
	@echo "$(GREEN)Демо использования CLI вентилятора:$(NC)"
	@echo "$(YELLOW)1. Запуск вентилятора:$(NC) ./$(BINARY_NAME) start"
	@echo "$(YELLOW)2. Запуск с определенной скоростью:$(NC) ./$(BINARY_NAME) start --speed 8"
	@echo "$(YELLOW)3. Установка скорости:$(NC) ./$(BINARY_NAME) speed 7"
	@echo "$(YELLOW)4. Остановка:$(NC) ./$(BINARY_NAME) stop"
	@echo "$(YELLOW)5. Справка:$(NC) ./$(BINARY_NAME) --help"
