import requests
import os
import time
import re

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"

# Используем XML фид — он самый стабильный и его не банят
URL_RSS = f"https://itunes.apple.com/ua/rss/customerreviews/id={APP_ID}/xml"

file_path = "version.txt"

print("--- СТАРТ ПРОВЕРКИ (RSS XML) ---")

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

print(f"В файле записано: {last_version}")

try:
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)'}
    response = requests.get(URL_RSS, headers=headers, timeout=15)
    
    # Ищем версию в XML коде через регулярку (ищем тег <im:version>)
    version_match = re.search(r'<im:version>([^<]+)</im:version>', response.text)
    
    if version_match:
        current_version = version_match.group(1).strip()
        print(f"✅ НАШЕЛ В App Store: {current_version}")

        # Сравниваем
        if current_version != last_version:
            print(f"!!! РАЗНИЦА ЕСТЬ! Отправляю 7 уведомлений...")
            
            for i in range(1, 8):
                text = f"🚨 ВЛАД, ОБНОВА! 🚨\nВерсия: {current_version}\n(Сигнал {i}/7)"
                r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                 json={"chat_id": CHAT_ID, "text": text})
                print(f"Отправка {i}: {r.status_code}")
                time.sleep(8)
            
            # Сохраняем новую версию
            with open(file_path, "w") as f:
                f.write(current_version)
        else:
            print("Версии одинаковые. Спим.")
            
    else:
        print("❌ ОШИБКА: Не нашел тег версии в ответе Apple.")
        # Если это принудительный тест (в файле стоит 1), шлем ошибку в телегу
        if last_version == "1" or last_version == "TEST":
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                         json={"chat_id": CHAT_ID, "text": "⚠️ Бот ослеп! Не вижу версию в XML!"})

except Exception as e:
    print(f"Критическая ошибка: {e}")
