import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1489715534"
URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua"

print(f"--- ТЕСТ СВЯЗИ ---")
print(f"Используем ID: {CHAT_ID}")

# 1. Пробуем отправить тестовое сообщение прямо сейчас
test_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
test_resp = requests.post(test_url, json={"chat_id": CHAT_ID, "text": "🔔 Тестовая проверка бота!"})

if test_resp.status_code == 200:
    print("✅ Успех! Telegram принял сообщение.")
else:
    print(f"❌ Ошибка Telegram: {test_resp.status_code}")
    print(f"Ответ сервера: {test_resp.text}")

# 2. Основная логика (чтобы версия в файле обновилась)
response = requests.get(URL).json()
if response.get('resultCount', 0) > 0:
    current_version = response['results'][0]['version']
    with open("version.txt", "w") as f:
        f.write(current_version)
    print(f"Версия Дії сохранена: {current_version}")
