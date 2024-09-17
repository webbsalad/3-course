package weather

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

type WeatherResponse struct {
	Weather []struct {
		Description string `json:"description"`
	} `json:"weather"`
	Main struct {
		Temp float64 `json:"temp"`
	} `json:"main"`
}

func Get(city string) (*WeatherResponse, string, error) {
	var cityName string
	switch city {
	case "Москва":
		cityName = "Moscow"
	case "Санкт-Петербург":
		cityName = "Saint%20Petersburg"
	case "Улан-Удэ":
		cityName = "Ulan-Ude"
	default:
		cityName = city
	}

	apiKey := os.Getenv("OPENWEATHERMAP_API_KEY")
	url := fmt.Sprintf("http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s", cityName, apiKey)
	resp, err := http.Get(url)
	if err != nil {
		return nil, url, err
	}
	defer resp.Body.Close()

	var weather WeatherResponse
	if err := json.NewDecoder(resp.Body).Decode(&weather); err != nil {
		return nil, url, err
	}

	return &weather, url, nil
}
