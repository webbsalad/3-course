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

class Currencies(metaclass=SingletonMeta):
    def __init__(self):
        self.__currencies = []

    def get_currencies(self, currencies_ids_lst):
        cur_res_str = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        result = []

        for _v in ET.fromstring(cur_res_str.content).findall("Valute"):
            valute_id = _v.get('ID')
            if str(valute_id) in currencies_ids_lst:
                valute_cur_name = _v.find('Name').text
                valute_cur_val = _v.find('Value').text.replace(',', '.')
                valute_charcode = _v.find('CharCode').text
                result.append({valute_charcode: (valute_cur_name, valute_cur_val)})

        self.__currencies = result

    def visualize_currencies(self):
        cur_codes = [list(currency.keys())[0] for currency in self.__currencies]
        cur_values = [float(list(currency.values())[0][1]) for currency in self.__currencies]

        plt.figure(figsize=(12, 6))
        plt.bar(cur_codes, cur_values, color='skyblue')
        plt.xlabel('Currency Code')
        plt.ylabel('Exchange Rate')
        plt.title('Exchange Rates')
        plt.savefig('currencies.jpg')
        plt.show()

if __name__ == '__main__':
    currencies_obj = Currencies()
    currencies_obj.get_currencies(['R01035', 'R01335', 'R01700J'])
    currencies_obj.visualize_currencies()
