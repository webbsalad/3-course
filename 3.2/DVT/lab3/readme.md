# 📖 Сторителлинг: «Как я искал идеальный серверный фреймворк»
Суворов Роман, Гневнов Артём, Анаминко С.с.

---

## 🖥️ **Введение**

Представьте, что вы разрабатываете веб-приложение, которое должны одновременно использовать тысячи пользователей. Система постоянно загружает и выгружает файлы разных размеров: от маленьких JSON-файлов до огромных архивов. И тут начинаются проблемы — сервер перестаёт справляться, пользователи жалуются на скорость, падает производительность. Передо мной, как разработчиком, встал вопрос: **«Какой серверный фреймворк обеспечит стабильность и производительность в таких условиях?»**

---

## 🎯 **Идея**

Моя главная задача была ясна: нужно выявить, какой фреймворк лучше всего справляется с обработкой смешанного набора файлов при разных нагрузках — последовательной и параллельной. Я решил провести исследование и сравнить четыре популярных фреймворка:

- **Go HTTP**
    
- **Gin**
    
- **FastAPI**
    
- **Flask**
    

---

## 🦸 **Герой**

Главный герой этой истории — не я сам, а **серверный фреймворк**, от выбора которого зависит успех всего проекта. Я должен был понять, какой из них сможет справиться с нагрузкой, останется стабильным и надёжным, несмотря ни на что.

---

## 🌍 **Проекция**

Вся история разворачивалась вокруг реальной ситуации, знакомой любому разработчику: серверы сталкиваются с разнообразными и непредсказуемыми нагрузками. Мой сценарий был прост — сервер должен устойчиво обрабатывать смешанный набор данных: от нескольких десятков мелких файлов до одного очень крупного объекта.

---

## 📈 **Сценарий исследования**

Для начала я подготовил тестовые сценарии, которые отражали реальные условия эксплуатации:

- Сервера обрабатывали от 10 до 1000 файлов.
    
- Нагрузка была как последовательной (файлы обрабатывались по очереди), так и параллельной (много запросов одновременно).
    
- Я фиксировал время загрузки и выгрузки данных для каждого сценария и каждого фреймворка.
    

---

## 🔬 **Путь к истине**

Чтобы облегчить сложные расчёты, я использовал мощный инструмент — аналитическую платформу **KNIME**, которая автоматизировала весь процесс анализа данных. Благодаря этому я получил не просто сухие цифры, а наглядные графики и точные коэффициенты корреляции.

Анализируя результаты, я заметил, что при последовательной обработке файлов все фреймворки демонстрировали стабильность. Но картина резко изменилась при параллельной обработке:

- **Flask** и **FastAPI** начали проявлять заметные колебания производительности.
    
- **Go HTTP** и **Gin** показали себя значительно стабильнее и быстрее.
    

---

## 📊 **Кульминация**

Самым интересным моментом стало сравнение отклонений производительности фреймворков в процентах и миллисекундах.

При последовательной обработке средние отклонения были умеренными у всех:

- Flask: **5.00%**
    
- FastAPI: **4.70%**
    
- Go HTTP: **7.74%**
    
- Gin: **10.49%**
    

Но в режиме параллельной обработки ситуация обострилась:

- Flask: **13.11%**
    
- FastAPI: **44.54%** (серьёзное ухудшение!)
    
- Go HTTP: **18.08%**
    
- Gin: **16.41%**
    

Однако, когда я посмотрел на абсолютные значения отклонений в миллисекундах, преимущество Go-фреймворков стало очевидным:

- Flask: до **384.35 мс**
    
- FastAPI: до **53.35 мс**
    
- Go HTTP: всего **1.72 мс**
    
- Gin: всего **1.82 мс**
    

Это был ключевой момент понимания: Go-фреймворки справлялись с параллельной нагрузкой гораздо лучше.

---

## 🌟 **Развязка**

В итоге мой анализ показал, что серверы на **Go HTTP и Gin** идеально подходят для проектов с высокой нагрузкой и многочисленными параллельными запросами. Они обеспечивают стабильность, низкие задержки и минимальные отклонения производительности.

Если ваш проект подразумевает более умеренные нагрузки, то можно использовать и Python-фреймворки (**Flask или FastAPI**). Но будьте готовы к потенциальным колебаниям производительности при интенсивной параллельной нагрузке.

---

## 🚀 **Мораль этой истории**

Эта история научила меня, что выбор серверного фреймворка не просто вопрос вкуса или привычки, а критическое решение, которое напрямую влияет на успех вашего приложения.

Теперь я знаю, как выбрать подходящий фреймворк — и вы тоже можете воспользоваться моими выводами, чтобы ваш сервер всегда работал идеально!

---