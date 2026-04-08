import requests
import os
import time
import re

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# Ссылка на обычную страницу в браузере
URL = "https://apps.apple.com/ua/app/%D0%B4%D1%96%D1%8F/id1483089069"

file_path = "version.txt"

print("--- ПРОВЕРКА ЧЕРЕЗ ВЕБ-СТРАНИЦУ ---")

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
    html_content = response.text
    
    # Ищем в коде страницы текст версии (например: "Версія 3.0.70")
    # Регулярка ищет цифры после слова "version" или внутри специфических тегов
    version_match = re.search(r'\"version\":\"([^\"]+)\"', html_content)
    
    if version_match:
        current_version = version_match.group(1).strip()
        print(f"✅ УСПЕХ! Нашел версию на странице: {current_version}")
        
        if current_version != last_version or last_version == "TEST":
            print(f"ОТПРАВЛЯЮ 10 СМС (Версия: {current_version})")
            for i in range(1, 11):
                msg = f"🚨 ВЛАД, ОБНОВА ДІЇ! 🚨\nВерсия: {current_version}\n(Сигнал {i}/10)"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             json={"chat_id": CHAT_ID, "text": msg})
                time.sleep(6)
            
            if last_version != "TEST":
                with open(file_path, "w") as f:
                    f.write(current_version)
        else:
            print("Версии совпадают. Все тихо.")
    else:
        print("❌ Не смог найти цифры версии на странице.")
        # Для теста - если не нашли, шлем ошибку в телегу
        if last_version == "TEST":
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                         json={"chat_id": CHAT_ID, "text": "⚠️ Бот не нашел версию в коде страницы!"})

except Exception as e:
    print(f"Ошибка: {e}")
