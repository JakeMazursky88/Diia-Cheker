import requests
import os
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"
URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua"

file_path = "version.txt"

# 1. Читаем версию из файла
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

try:
    # 2. Проверяем App Store
    response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15).json()
    if response.get('resultCount', 0) > 0:
        current_version = str(response['results'][0]['version']).strip()
        
        # 3. Если версия ОБНОВИЛАСЬ
        if current_version != last_version:
            # ЦИКЛ НА 10 УВЕДОМЛЕНИЙ (РОВНО 1 МИНУТА ТРЯСКИ)
            for i in range(10):
                text = f"🚨 ВЛАД, ПОДЪЕМ! ДІЯ ОБНОВИЛАСЬ! 🚨\nВерсия: {current_version}\n(Сигнал {i+1}/10 — Трясу телефон 1 минуту)"
                
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             json={"chat_id": CHAT_ID, "text": text})
                
                # Пауза 6 секунд, чтобы длинная вибрация iPhone успела полностью отработать
                time.sleep(6) 
            
            # Сохраняем новую версию только ПОСЛЕ того, как "отзвонили"
            with open(file_path, "w") as f:
                f.write(current_version)
                
except Exception as e:
    print(f"Ошибка: {e}")
