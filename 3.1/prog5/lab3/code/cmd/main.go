package main

import (
	"log"

	"github.com/webbsalad/go-weather-bot/bot"
	"github.com/webbsalad/go-weather-bot/config"
)

func main() {
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatal(err)
	}

	b := bot.NewBot(cfg.TelegramToken)
	b.Start()
}
