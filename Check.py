import requests
import os
import time
import re

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"
# ИСПОРАВЛЕНО: только https
URL_WEB = f"https://apps.apple.com/ua/app/id{APP_ID}"

file_path = "version.txt"

def send_alert(ver):
    print(f"--- ЗАПУСК ОПОВЕЩЕНИЯ (Версия: {ver}) ---")
    # 10 сообщений, пауза 6 сек = 1 минута вибрации
    for i in range(1, 11):
        text = f"🚨 ВЛАД, ПОДЪЕМ! ДІЯ {ver}! 🚨\nСигнал {i}/10"
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                         json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        except: pass
        time.sleep(6)
    
    with open(file_path, "w") as f:
        f.write(ver)

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

print(f"--- СИСТЕМА 'ПЕРЕХВАТ' (В файле: {last_version}) ---")

current_version = None

try:
    # Заголовки как у браузера на Windows (самые стабильные для парсинга)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    response = requests.get(URL_WEB, headers=headers, timeout=20)
    html = response.text

    # Ищем версию в JSON-блоках страницы
    patterns = [
        r'\"softwareVersion\":\"([^\"]+)\"',
        r'\"version\":\"([^\"]+)\"',
        r'version-history__item__version-number\">([^<]+)<'
    ]

    for p in patterns:
        match = re.search(p, html)
        if match:
            found = match.group(1).strip()
            # Оставляем только цифры и точки
            found = re.sub(r'[^\d\.]', '', found)
            if found and len(found) > 2:
                current_version = found
                print(f"✅ Нашел версию: {current_version}")
                break

    if current_version:
        # Если в файле стоит 1 — это принудительный тест
        if current_version != last_version or last_version == "1":
            send_alert(current_version)
        else:
            print("Версии совпадают. Спим.")
    else:
        print("❌ ПРОВАЛ: Не нашел версию в коде. Apple поменяла структуру.")
        if last_version == "1":
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                         json={"chat_id": CHAT_ID, "text": "⚠️ Бот всё еще не видит цифры версии на сайте!"})

except Exception as e:
    print(f"Критическая ошибка: {e}")
    if last_version == "1":
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                     json={"chat_id": CHAT_ID, "text": f"Ошибка в коде: {e}"})
