import requests
import os
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ТЕСТОВЫЙ ЗАПУСК - ИГНОРИРУЕМ ВЕРСИИ
print("--- ЗАПУСКАЮ ТЕСТ СВЯЗИ С ТЕЛЕГРАМОМ ---")

for i in range(5):
    text = f"🚀 ТЕСТ СВЯЗИ! Сообщение {i+1}/5\nЕсли ты это видишь, значит бот работает!"
    res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                         json={"chat_id": CHAT_ID, "text": text})
    print(f"Ответ Телеграма: {res.status_code}")
    time.sleep(1)

print("--- ТЕСТ ЗАВЕРШЕН ---")
