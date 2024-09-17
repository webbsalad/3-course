package bot

import (
	"fmt"
	"log"

	tgbot "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/webbsalad/go-weather-bot/pkg/weather"
)

type Bot struct {
	api *tgbot.BotAPI
}

func NewBot(token string) *Bot {
	bot, err := tgbot.NewBotAPI(token)
	if err != nil {
		log.Panic(err)
	}

	return &Bot{api: bot}
}

func (b *Bot) Start() {
	u := tgbot.NewUpdate(0)
	u.Timeout = 60

	updates := b.api.GetUpdatesChan(u)

	for update := range updates {
		if update.Message != nil {
			if update.Message.IsCommand() {
				b.handleCommand(update.Message)
			} else if update.Message.Text != "" {
				b.handleText(update.Message)
			}
		}
	}
}

func (b *Bot) handleCommand(message *tgbot.Message) {
	switch message.Command() {
	case "start":
		buttons := tgbot.NewReplyKeyboard(
			tgbot.NewKeyboardButtonRow(
				tgbot.NewKeyboardButton("Москва"),
				tgbot.NewKeyboardButton("Санкт-Петербург"),
				tgbot.NewKeyboardButton("Улан-Удэ"),
			),
		)
		msg := tgbot.NewMessage(message.Chat.ID, "Выберите город, чтобы узнать погоду:")
		msg.ReplyMarkup = buttons
		b.api.Send(msg)
	default:
		msg := tgbot.NewMessage(message.Chat.ID, "Не знаю такой команды")
		b.api.Send(msg)
	}
}

func (b *Bot) handleText(message *tgbot.Message) {
	city := message.Text
	log.Printf("Получено обращение: %s", city)

	weatherData, requestUrl, err := weather.Get(city)
	log.Printf("Запрос к OpenWeatherMap: %s", requestUrl)

	if err != nil {
		msg := tgbot.NewMessage(message.Chat.ID, "Извините, не удалось получить погоду.")
		b.api.Send(msg)
		log.Printf("Ошибка при получении данных о погоде: %v", err)
		return
	}

	if len(weatherData.Weather) == 0 {
		msg := tgbot.NewMessage(message.Chat.ID, "Извините, нет информации о погоде.")
		b.api.Send(msg)
		log.Println("Ответ от OpenWeatherMap: нет информации о погоде.")
		return
	}

	response := fmt.Sprintf("%s:\nТемпература: %.2f°C\nОписание: %s", city, weatherData.Main.Temp-273.15, weatherData.Weather[0].Description)
	msg := tgbot.NewMessage(message.Chat.ID, response)
	b.api.Send(msg)

	log.Printf("Ответ от OpenWeatherMap: Температура: %.2f°C, Описание: %s", weatherData.Main.Temp-273.15, weatherData.Weather[0].Description)
	log.Printf("Отправлено сообщение в Telegram: %s", response)
}
