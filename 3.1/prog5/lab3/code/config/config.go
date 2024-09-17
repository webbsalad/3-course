package config

import (
	"os"

	"github.com/joho/godotenv"
)

type Config struct {
	TelegramToken        string
	OpenWeatherMapAPIKey string
}

func LoadConfig() (*Config, error) {
	err := godotenv.Load()
	if err != nil {
		return nil, err
	}

	return &Config{
		TelegramToken:        os.Getenv("TELEGRAM_BOT_API_TOKEN"),
		OpenWeatherMapAPIKey: os.Getenv("OPENWEATHERMAP_API_KEY"),
	}, nil
}
