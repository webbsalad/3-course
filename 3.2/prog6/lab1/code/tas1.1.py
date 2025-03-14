import pandas as pd
import matplotlib.pyplot as plt

marketing_data = pd.read_csv('./data/MarketingSpend.csv', header=0, names=['Date', 'Offline', 'Online'])
retail_data = pd.read_csv('./data/Retail.csv')

print("статистика по online spend:")
print(f"максимальное значение: {marketing_data['Online'].max()}")
print(f"минимальное значение: {marketing_data['Online'].min()}")
print(f"среднее значение: {marketing_data['Online'].mean():.3f}")
print(f"медиана: {marketing_data['Online'].median():.3f}")
print(f"стандартное отклонение (std): {marketing_data['Online'].std():.3f}")
print(f"дисперсия: {marketing_data['Online'].var():.3f}")

print("\nстатистика по offline spend:")
print(f"максимальное значение: {marketing_data['Offline'].max()}")
print(f"минимальное значение: {marketing_data['Offline'].min()}")
print(f"среднее значение: {marketing_data['Offline'].mean():.3f}")
print(f"медиана: {marketing_data['Offline'].median():.3f}")
print(f"стандартное отклонение (std): {marketing_data['Offline'].std():.3f}")
print(f"дисперсия: {marketing_data['Offline'].var():.3f}")

print("\nобщая статистика по marketingSpend.csv:")
print(marketing_data.describe())

plt.figure(figsize=(12, 6))

marketing_data['Online'].hist(bins=100, alpha=0.5, color='blue', label='online spend', density=True)
marketing_data['Offline'].hist(bins=100, alpha=0.5, color='red', label='offline spend', density=True)

plt.title("распределение маркетинговых затрат (online vs offline) - 100 bins")
plt.xlabel("сумма затрат")
plt.ylabel("плотность")
plt.legend()
plt.grid(True)

print("\nинформация о датасете marketingSpend.csv:")
print(marketing_data.info())

print('-' * 80)

print("\nобщая статистика по retail.csv:")
print(retail_data.describe())

num_invoices = len(retail_data['InvoiceNo'].unique())
print(f"\nколичество уникальных инвойсов: {num_invoices}")

num_stockcodes = len(retail_data['StockCode'].unique())
print(f"количество уникальных товаров (stockCode): {num_stockcodes}")

top_10_stockcodes = retail_data['StockCode'].value_counts().head(10)
print("\nтоп-10 самых заказываемых товаров (stockCode):")
print(top_10_stockcodes)

print('-' * 80)
plt.show()
