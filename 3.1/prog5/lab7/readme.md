# Суворов Роман ИВТ 2.1
## Прог Лабораторная работа №8

### Описание

Код реализует шаблон проектирования "Наблюдатель" (Observer) для получения и распространения данных о курсах валют через WebSocket-соединение в FastAPI. Программа запрашивает курсы валют у Центробанка, сравнивает с последними полученными значениями и отправляет изменения зарегистрированным клиентам. 

### Структура программы

1. **Объект**: Сервер FastAPI, который взаимодействует с API Центробанка и сохраняет текущие курсы валют. Обновления данных происходят через фиксированные интервалы времени.
2. **Наблюдатели**: WebSocket-клиенты, подключенные к серверу, которые получают уведомления об изменениях курсов в реальном времени.
3. **Логика уведомлений**: Сервер запрашивает данные у Центробанка каждые 10 секунд, сравнивая изменения и отправляя обновления.

### Основные функции

1. **Запрос валютных курсов**: Асинхронная функция запрашивает данные у API Центробанка и возвращает их в формате JSON.
2. **Рассылка обновлений**: При изменении курсов функция пересылает данные всем подключенным WebSocket-клиентам. Если изменения не обнаружены, данные не отправляются. Пример функции уведомления
### Пример использования

- Клиенты подключаются через WebSocket, отправляя запрос к `/ws`. Каждый клиент отображает данные валют на HTML-странице.
    
- **Пример формата получаемых данных**:
```
{ "AUD": 63.8946, "AZN": 57.2506, "GBP": 126.485, "AMD": 25.145, "BYN": 29.3797, "BGN": 53.8326, "BRL": 17.0792, "HUF": 26.0251, "VND": 40.1312, "HKD": 12.5485, "GEL": 35.7094, "DKK": 14.1165, "AED": 26.5013, "USD": 97.3261, "EUR": 105.4375, "EGP": 19.9807, "INR": 11.5757, "IDR": 61.8769, "KZT": 19.9516, "CAD": 70.044, "QAR": 26.7379, "KGS": 11.3434, "CNY": 13.5954, "MDL": 54.1055, "NZD": 58.1718, "NOK": 88.3875, "PLN": 24.1798, "RON": 21.1413, "XDR": 129.4135, "SGD": 73.4537, "TJS": 91.3226, "THB": 28.8211, "TRY": 28.4415, "TMT": 27.8075, "UZS": 76.0662, "UAH": 23.549, "CZK": 41.7154, "SEK": 91.7857, "CHF": 112.3598, "RSD": 89.9107, "ZAR": 54.9644, "KRW": 70.1702, "JPY": 63.6451 }
```
