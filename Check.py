import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = [os.getenv("TELEGRAM_CHAT_ID"), os.getenv("FRIEND_CHAT_ID")]
APP_ID = "1489715534"
URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua"

# Читаем, какая версия была в прошлый раз
try:
    with open("version.txt", "r") as f:
        last_version = f.read().strip()
except FileNotFoundError:
    last_version = ""

try:
    response = requests.get(URL).json()
    if response.get('resultCount', 0) > 0:
        current_version = response['results'][0]['version']

        # Если версия изменилась — бьем тревогу
        if current_version != last_version:
            msg = f"🚀 Вышло обновление Дії! Новая версия: {current_version}"
            for chat_id in CHAT_IDS:
                if chat_id:
                    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}")
            
            # Запоминаем новую версию
            with open("version.txt", "w") as f:
                f.write(current_version)
except Exception as e:
    print(f"Ошибка: {e}")
