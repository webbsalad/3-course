---
transition: fade
theme: solarized
highlightTheme: github
progress: true
controls: false
backgroundTransition: fade
slideNumber: true
height: "700"
width: "1000"
---


# **Bounded Semaphore**  

---
### **Что такое семафор?**
✅ Ограничивает число одновременных горутин/корутин  
❌ Не проверяет правильность освобождения

---

### **Bounded Semaphore**

 ✅ Контроль за состоянием  
 ⚠️ Panic/Exception/ValueError
 
---

### Псевдокод: обычный семафор
```
Функция Acquire:
    положить токен в канал/queue

Функция Release:
    взять токен из канала/queue


```

---

### **Псевдокод: bounded semaphore**

```
Функция Acquire:
    положить токен в канал
    held += 1

Функция Release:
    если held <= 0:
        panic("release без acquire")
    held -= 1
    взять токен из канала

```

---

### **Зачем нужен контроль?**

🔍 Быстрая отладка  
🧠 Явная логика  
🛡️ Безопасность в продакшене

---

# Итоги
