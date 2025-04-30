import timeit
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import importlib.util
import os
import time
import signal

# Функция-обработчик для ограничения времени выполнения
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Превышено время выполнения")

# Компилируем Cython модуль
print("Компиляция Cython модуля...")
subprocess.run(["python", "setup.py", "build_ext", "--inplace"], check=True)

# Импортируем Cython модуль
import ferma_fact # type: ignore
from main import fermat_factorization as py_fermat_factorization, is_perfect_square

# Тестовые числа (уменьшенный список, содержащий только небольшие числа)
TEST_LST = [101, 9973, 104729, 101909, 609133]
REPEAT = 3
NUMBER = 5

# Проверка, что обе реализации дают одинаковый результат
print("Проверка корректности...")
for num in TEST_LST[:5]:  # Проверим на первых 5 числах
    py_result = py_fermat_factorization(num)
    cy_result = ferma_fact.fermat_factorization(num)
    assert py_result == cy_result, f"Разные результаты для {num}: Python {py_result}, Cython {cy_result}"

print("Измерение времени выполнения...")

# Измерение времени Python версии
try:
    py_times = timeit.repeat(
        "res = [py_fermat_factorization(i) for i in TEST_LST]",
        setup='from __main__ import py_fermat_factorization, TEST_LST',
        number=NUMBER,
        repeat=REPEAT
    )
    py_best = min(py_times)
except Exception as e:
    print(f"Ошибка при измерении времени Python версии: {e}")
    py_best = float('inf')  # Если произошла ошибка, устанавливаем "бесконечное" время

# Измерение времени Cython версии
try:
    cy_times = timeit.repeat(
        "res = [ferma_fact.fermat_factorization(i) for i in TEST_LST]",
        setup='from __main__ import ferma_fact, TEST_LST',
        number=NUMBER,
        repeat=REPEAT
    )
    cy_best = min(cy_times)
except Exception as e:
    print(f"Ошибка при измерении времени Cython версии: {e}")
    cy_best = float('inf')  # Если произошла ошибка, устанавливаем "бесконечное" время

# Проверка, что у нас есть результаты для обеих версий
if py_best == float('inf') and cy_best == float('inf'):
    print("Не удалось измерить время выполнения ни для одной версии")
    exit(1)
elif py_best == float('inf'):
    print("Не удалось измерить время выполнения Python версии")
    speedup = float('inf')
elif cy_best == float('inf'):
    print("Не удалось измерить время выполнения Cython версии")
    speedup = 0
else:
    speedup = py_best / cy_best

print(f"Время выполнения Python: {py_best:.5f} секунд")
print(f"Время выполнения Cython: {cy_best:.5f} секунд")
print(f"Ускорение: {speedup:.2f}x")

# Построение графика
labels = ['Python', 'Cython']
times = [py_best if py_best != float('inf') else 0, cy_best if cy_best != float('inf') else 0]
colors = ['blue', 'green']

plt.figure(figsize=(10, 6))
plt.bar(labels, times, color=colors, width=0.5)
plt.title('Сравнение производительности Python и Cython')
plt.xlabel('Реализация')
plt.ylabel('Время выполнения (сек)')

for i, v in enumerate(times):
    if v > 0:  # Только если время не бесконечное
        plt.text(i, v + 0.05, f"{v:.5f} сек", ha='center')
    else:
        plt.text(i, 0.05, "Timeout", ha='center')

plt.savefig('performance_comparison.png')
plt.tight_layout()
plt.show()

# Тестирование отдельных чисел
print("\nТестирование отдельных чисел:")
# Список тестовых чисел с разными размерами
test_numbers = [101, 9973, 104729]
results = []

# Установка обработчика сигнала для ограничения времени выполнения
signal.signal(signal.SIGALRM, timeout_handler)

for num in test_numbers:
    print(f"\nТестирование числа: {num}")
    
    # Тестирование Python-версии
    try:
        signal.alarm(10)  # Лимит 10 секунд
        start = time.time()
        py_result = py_fermat_factorization(num)
        py_time = time.time() - start
        signal.alarm(0)  # Отключаем таймер
        print(f"Python: {py_time:.5f} сек, результат: {py_result}")
    except TimeoutException:
        print("Python: превышено время выполнения (>10 сек)")
        py_time = float('inf')
    except Exception as e:
        print(f"Python: ошибка - {e}")
        py_time = float('inf')
    
    # Тестирование Cython-версии
    try:
        signal.alarm(10)  # Лимит 10 секунд
        start = time.time()
        cy_result = ferma_fact.fermat_factorization(num)
        cy_time = time.time() - start
        signal.alarm(0)  # Отключаем таймер
        print(f"Cython: {cy_time:.5f} сек, результат: {cy_result}")
    except TimeoutException:
        print("Cython: превышено время выполнения (>10 сек)")
        cy_time = float('inf')
    except Exception as e:
        print(f"Cython: ошибка - {e}")
        cy_time = float('inf')
    
    # Если оба времени конечны, считаем ускорение
    if py_time != float('inf') and cy_time != float('inf'):
        speedup = py_time / cy_time
        print(f"Ускорение: {speedup:.2f}x")
    
    results.append((num, py_time, cy_time))

# Построение графика для отдельных чисел
if results:
    plt.figure(figsize=(12, 6))
    
    numbers = [str(r[0]) for r in results]
    py_times = [r[1] if r[1] != float('inf') else 0 for r in results]
    cy_times = [r[2] if r[2] != float('inf') else 0 for r in results]
    
    x = np.arange(len(numbers))
    width = 0.35
    
    plt.bar(x - width/2, py_times, width, label='Python', color='blue')
    plt.bar(x + width/2, cy_times, width, label='Cython', color='green')
    
    plt.xlabel('Число')
    plt.ylabel('Время выполнения (сек)')
    plt.title('Сравнение производительности для отдельных чисел')
    plt.xticks(x, numbers)
    plt.legend()
    
    plt.savefig('individual_comparisons.png')
    plt.tight_layout()
    plt.show()

print("\nТестирование завершено. Результаты сохранены в файлах performance_comparison.png и individual_comparisons.png.")