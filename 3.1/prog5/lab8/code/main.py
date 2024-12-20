import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

def get_weather_data(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Ошибка получения данных:", response.json())
        return None
    data = response.json()
    weather_data = [
        {
            "datetime": item["dt_txt"],
            "temperature": item["main"]["temp"]
        }
        for item in data["list"]
    ]
    return weather_data

def visualize_weather_data(weather_df):
    weather_df["datetime"] = pd.to_datetime(weather_df["datetime"])
    plt.figure(figsize=(12, 6))
    plt.scatter(weather_df["datetime"], weather_df["temperature"], alpha=0.7)
    plt.title("Температура за последние дни")
    plt.xlabel("Дата и время")
    plt.ylabel("Температура (°C)")
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()
    plt.figure(figsize=(6, 8))
    plt.boxplot(weather_df["temperature"], vert=True, patch_artist=True)
    plt.title("Диаграмма температур (boxplot)")
    plt.ylabel("Температура (°C)")
    plt.grid()
    plt.show()

api_key = os.getenv("API_KEY")
lat = 59.57
lon = 30.19

weather_data = get_weather_data(api_key, lat, lon)
if weather_data:
    weather_df = pd.DataFrame(weather_data)
    print(weather_df.head())
    visualize_weather_data(weather_df)
