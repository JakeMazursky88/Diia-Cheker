import requests
import os
import time

# Берем данные из твоих Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print("--- ЗАПУСК ПРОВЕРКИ ТОКЕНА ---")
print(f"Пытаюсь отправить на ID: {CHAT_ID}")

for i in range(1, 6):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID, 
            "text": f"🔔 ТЕСТ СВЯЗИ #{i}\nЕсли видишь это — токен ЖИВОЙ!"
        }
        r = requests.post(url, json=data, timeout=10)
        
        # Выводим в лог результат каждой попытки
        print(f"Попытка {i}: Статус {r.status_code}, Ответ: {r.text}")
        
    except Exception as e:
        print(f"Ошибка на попытке {i}: {e}")
    
    # Пауза 10 секунд между сообщениями, чтобы не злить фильтры
    time.sleep(10)

print("--- ПРОВЕРКА ЗАВЕРШЕНА ---")
