import requests
import os
import time
import re

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# Ссылка на страницу Дії на стороннем сервисе
URL = "https://iphone.apkpure.com/ua/%D0%B4%D1%96%D1%8F/id1483089069"

file_path = "version.txt"

print("--- ПРОВЕРКА ЧЕРЕЗ АГРЕГАТОР ---")

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(URL, headers=headers, timeout=20)
    
    # Ищем версию на странице. Обычно она в теге с классом "version" или рядом
    # Ищем паттерн типа "Version: 4.31.7"
    version_match = re.search(r'Version\s*</span>\s*<span>([\d\.]+)', response.text, re.IGNORECASE)
    
    # Если первый паттерн не сработал, ищем просто любые цифры версии в коде
    if not version_match:
        version_match = re.search(r'\"version\":\"([\d\.]+)\"', response.text)

    if version_match:
        current_version = version_match.group(1).strip()
        print(f"✅ УСПЕХ! На агрегаторе версия: {current_version}")

        if current_version != last_version:
            print(f"РАЗНИЦА! Шлю 7 смс...")
            for i in range(1, 8):
                text = f"🚨 ВЛАД, ОБНОВА ДІЇ! 🚨\nВерсия: {current_version}\n(Сигнал {i}/7)"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             json={"chat_id": CHAT_ID, "text": text})
                time.sleep(8)
            
            with open(file_path, "w") as f:
                f.write(current_version)
        else:
            print("Версии совпали.")
    else:
        print("❌ Агрегатор тоже не отдал версию.")
        if last_version == "1":
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                         json={"chat_id": CHAT_ID, "text": "⚠️ Даже агрегатор не видит версию!"})

except Exception as e:
    print(f"Ошибка: {e}")
