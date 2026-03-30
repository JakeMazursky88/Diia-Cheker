import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
# Собираем ID (твой и друга), убираем пустые
CHAT_IDS = [id for id in [os.getenv("TELEGRAM_CHAT_ID"), os.getenv("FRIEND_CHAT_ID")] if id]

APP_ID = "1489715534"
URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua"

# Читаем старую версию
if os.path.exists("version.txt"):
    with open("version.txt", "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

try:
    response = requests.get(URL, timeout=15).json()
    if response.get('resultCount', 0) > 0:
        current_version = response['results'][0]['version']
        
        # Если в App Store версия новее, чем у нас в файле
        if current_version != last_version:
            msg = f"🚀 Обновление Дії!\nНовая версия: {current_version}"
            
            for chat_id in CHAT_IDS:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             json={"chat_id": chat_id, "text": msg})
            
            # Записываем новую версию в файл
            with open("version.txt", "w") as f:
                f.write(current_version)
            print(f"Обновлено до {current_version}")
        else:
            print(f"Версия не менялась: {current_version}")
except Exception as e:
    print(f"Ошибка: {e}")
