import requests
import os
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"
URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua"

file_path = "version.txt"

# 1. Читаем старую версию
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

print("--- ПРОВЕРКА ВЕРСИИ ДІЇ (РЕЖИМ 1 МИНУТА) ---")

try:
    # 2. Запрос в App Store
    response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15).json()
    
    if response.get('resultCount', 0) > 0:
        current_version = str(response['results'][0]['version']).strip()
        print(f"Версия в магазине: {current_version}")
        
        # 3. СРАВНЕНИЕ
        if current_version != last_version:
            print("!!! ОБНОВЛЕНИЕ НАЙДЕНО !!!")
            
            # ЦИКЛ НА 1 МИНУТУ (20 сообщений по 3 сек паузы)
            for i in range(20):
                text = f"🚨 ВЛАД! ДІЯ ОБНОВИЛАСЬ! 🚨\nВерсия: {current_version}\n(Сигнал {i+1}/20 — Трясу телефон 1 минуту)"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             json={"chat_id": CHAT_ID, "text": text})
                
                # Пауза 3 секунды, чтобы длинная вибрация iPhone успела отработать
                time.sleep(3) 
            
            # Сохраняем новую версию только после того, как "отзвонили"
            with open(file_path, "w") as f:
                f.write(current_version)
            print("Версия обновлена, спам завершен.")
        else:
            print("Изменений нет. Тишина.")
    else:
        print("Ошибка данных App Store.")

except Exception as e:
    print(f"Ошибка: {e}")
