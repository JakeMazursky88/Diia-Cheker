import requests
import os
import time
import re

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"
# Ссылка на украинский стор
URL_WEB = f"https://apps.apple.com/ua/app/id{APP_ID}"

file_path = "version.txt"

def send_alert(ver):
    print(f"--- ЗАПУСК ОПОВЕЩЕНИЯ (Версия: {ver}) ---")
    # 10 сообщений с паузой 6 секунд (ровно 1 минута вибрации)
    for i in range(1, 11):
        text = f"🚨 ВЛАД, ПОДЪЕМ! ДІЯ {ver}! 🚨\nСигнал {i}/10"
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                         json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        except: pass
        time.sleep(6)
    
    with open(file_path, "w") as f:
        f.write(ver)

# 1. Читаем старую версию
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

print(f"--- СИСТЕМА 'ПЕРЕХВАТ' (В файле: {last_version}) ---")

current_version = None

try:
    # 2. Идем на страницу с заголовками реального iPhone
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
    }
    response = requests.get(URL_WEB, headers=headers, timeout=20)
    html = response.text

    # 3. Ищем версию в 3 разных паттернах (Apple прячет её в JSON)
    patterns = [
        r'\"softwareVersion\":\"([^\"]+)\"',        # JSON-LD формат
        r'\"version\":\"([^\"]+)\"',                # Обычный JSON
        r'version-history__item__version-number\">([^<]+)<' # Текстовый блок истории
    ]

    for p in patterns:
        match = re.search(p, html)
        if match:
            current_version = match.group(1).strip()
            # Убираем лишние слова, если они попали (оставляем только цифры и точки)
            current_version = re.sub(r'[^\d\.]', '', current_version)
            if current_version:
                print(f"✅ Нашел версию: {current_version}")
                break

    # 4. СРАВНЕНИЕ
    if current_version:
        if current_version != last_version or last_version == "1":
            send_alert(current_version)
        else:
            print("Версии совпадают. Обновлений нет.")
    else:
        print("❌ ПРОВАЛ: Код страницы пришел, но данных о версии внутри нет.")
        if last_version == "1":
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                         json={"chat_id": CHAT_ID, "text": "⚠️ Бот не видит версию даже в коде страницы!"})

except Exception as e:
    print(f"Ошибка: {e}")
    if last_version == "1":
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                     json={"chat_id": CHAT_ID, "text": f"Ошибка скрипта: {e}"})
