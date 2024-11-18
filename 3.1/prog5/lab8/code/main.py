import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from io import StringIO

load_dotenv()

def getweather():
    import json
    import requests
    from datetime import datetime, timedelta

    city, lat, lon = "Saint Petersburg, RU", 59.57, 30.19

    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        api_key = input('Введите ваш API ключ OpenWeatherMap: ')
        with open('.env', 'a') as f:
            f.write(f'\nOPENWEATHER_API_KEY={api_key}')
        load_dotenv() 

    current_time = datetime.now()
    result = {
        'city': city,
        'temps': []
    }

    for i in range(5):
        day_time = current_time - timedelta(days=i+1)
        dt = int(day_time.replace(hour=12, minute=0, second=0).timestamp())

        url = 'https://api.openweathermap.org/data/2.5/onecall/timemachine'
        params = {
            'lat': lat,
            'lon': lon,
            'dt': dt,
            'appid': api_key,
            'units': 'metric',
            'lang': 'ru'
        }

        req = requests.get(url, params=params)

        if req.status_code != 200:
            print(f"Ошибка при запросе данных за {day_time.strftime('%Y-%m-%d')}: {req.status_code}")
            print(req.text)
            continue

        req_obj = req.json()

        for hour_data in req_obj['hourly']:
            result['temps'].append({
                'dt': str(hour_data['dt']),
                'temp': str(hour_data['temp'])
            })

    return json.dumps(result)

weather_data_json = getweather()

def visualise_data(json_data=''):
    if json_data:
        import matplotlib.pyplot as plt
        import pandas as pd
        from datetime import datetime
        from io import StringIO

        data = pd.read_json(StringIO(json_data))
        city_name = data['city']

        dates = [datetime.fromtimestamp(int(d['dt'])) for d in data['temps']]
        temps = [float(t['temp']) for t in data['temps']]

        df = pd.DataFrame({'Дата и время': dates, 'Температура': temps})

        plt.figure(figsize=(12, 6))
        plt.scatter(df['Дата и время'], df['Температура'], color='blue')
        plt.title(f'Температура в {city_name} за последние 5 дней')
        plt.xlabel('Дата и время')
        plt.ylabel('Температура (°C)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()

        plt.figure(figsize=(6, 8))
        plt.boxplot(df['Температура'], vert=True, patch_artist=True)
        plt.title('Распределение температур за последние 5 дней')
        plt.ylabel('Температура (°C)')
        plt.grid(True)
        plt.show()

visualise_data(weather_data_json)
