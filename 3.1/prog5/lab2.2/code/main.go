package main

import (
	"fmt"

	"github.com/webbsalad/go-weather-bot/bot"
	"github.com/webbsalad/go-weather-bot/config"
)

func main() {
	fmt.Println("https://t.me/gowea_bot")

	cfg, _ := config.LoadConfig()

	b := bot.NewBot(cfg.TelegramToken)
	b.Start()

}
