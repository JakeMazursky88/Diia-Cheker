import requests
import os
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"
# Самый стабильный источник данных от Apple
URL_RSS = f"https://itunes.apple.com/ua/rss/customerreviews/id={APP_ID}/json"

file_path = "version.txt"

# 1. Читаем старую версию
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

try:
    # 2. Получаем данные
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL_RSS, headers=headers, timeout=15).json()
    
    # 3. Вытаскиваем версию из фида
    entries = response.get('feed', {}).get('entry', [])
    if entries:
        current_version = entries[0].get('im:version', {}).get('label', '').strip()
        
        print(f"Версия в App Store: {current_version} (В файле: {last_version})")

        # 4. СРАВНЕНИЕ (или тест, если в файле написано TEST)
        if current_version != last_version or last_version == "TEST":
            print("ОБНОВА! Запускаю серию СМС...")
            
            # Серия из 7 сообщений с паузой 8 секунд (итого ~1 минута вибрации)
            for i in range(1, 8):
                text = f"🚨 ВЛАД, ПОДЪЕМ! ДІЯ {current_version}! 🚨\nСигнал {i} из 7"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             json={"chat_id": CHAT_ID, "text": text})
                time.sleep(8)
            
            # Сохраняем новую версию, чтобы не спамить бесконечно
            if last_version != "TEST":
                with open(file_path, "w") as f:
                    f.write(current_version)
        else:
            print("Изменений нет.")
    else:
        print("RSS-фид пуст. Apple вредничает.")

except Exception as e:
    print(f"Ошибка: {e}")
