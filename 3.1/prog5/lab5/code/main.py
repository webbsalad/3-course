import requests
from xml.etree import ElementTree as ET
import time
import matplotlib.pyplot as plt


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CurrencyFetcher(metaclass=SingletonMeta):
    def __init__(self):
        self.last_request_time = 0
        self.currencies = []

    def get_currencies(self, currencies_ids_lst):
        current_time = time.time()
        if current_time - self.last_request_time < 1:
            raise Exception("Запросы можно делать не чаще, чем раз в секунду.")
        self.last_request_time = current_time

        response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        root = ET.fromstring(response.content)
        self.currencies = []
        for valute in root.findall('Valute'):
            valute_id = valute.get('ID')
            if valute_id in currencies_ids_lst:
                name = valute.find('Name').text
                value = valute.find('Value').text.replace(',', '.')
                charcode = valute.find('CharCode').text
                nominal = int(valute.find('Nominal').text)
                value_per_unit = float(value) / nominal
                self.currencies.append({charcode: (name, f"{value_per_unit:.4f}")})
        return self.currencies

    def visualize_currencies(self):
        fig, ax = plt.subplots()
        charcodes = [list(item.keys())[0] for item in self.currencies]
        values = [float(list(item.values())[0][1]) for item in self.currencies]

        ax.bar(charcodes, values, color='blue')
        ax.set_xlabel('Валюта')
        ax.set_ylabel('Курс (в рублях)')
        ax.set_title('Курсы валют')
        plt.show()


if __name__ == '__main__':
    fetcher = CurrencyFetcher()
    try:
        result = fetcher.get_currencies(['R01035', 'R01335', 'R01700J'])
        print(result)
        fetcher.visualize_currencies()
    except Exception as e:
        print(e)
