import requests
import os
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"

# Ссылка на API
URL_API = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua"

file_path = "version.txt"

# 1. Читаем версию из файла
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

print(f"В файле записано: {last_version}")

def send_alert(version):
    print(f"!!! НАШЕЛ ОБНОВУ: {version} !!!")
    for i in range(1, 11):
        text = f"🚨 ВЛАД, ПОДЪЕМ! ДІЯ {version}! 🚨\nСигнал {i}/10"
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                     json={"chat_id": CHAT_ID, "text": text})
        time.sleep(6)
    with open(file_path, "w") as f:
        f.write(version)

try:
    # ПОПЫТКА 1: Обычный запрос
    print("Пробую Попытку 1...")
    res = requests.get(URL_API, timeout=15).json()
    if res.get('resultCount', 0) > 0:
        current_version = str(res['results'][0]['version']).strip()
        if current_version != last_version:
            send_alert(current_version)
            exit()
        else:
            print("Версии совпали в API")
    
    # ПОПЫТКА 2: Если API выдал пустоту, пробуем через веб-страницу (как браузер)
    print("Попытка 1 провалена, пробую Попытку 2 (Веб)...")
    web_url = f"https://apps.apple.com/ua/app/id{APP_ID}"
    web_res = requests.get(web_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15).text
    import re
    # Ищем версию в тексте страницы
    match = re.search(r'\"version\":\"([^\"]+)\"', web_res)
    if match:
        current_version = match.group(1).strip()
        print(f"Нашел версию на странице: {current_version}")
        if current_version != last_version:
            send_alert(current_version)
            exit()
    
    # ПОПЫТКА 3: Принудительный тест, если ты написал TEST
    if last_version == "TEST":
        send_alert("ТЕСТОВАЯ")

except Exception as e:
    print(f"Ошибка: {e}")
    # Если совсем всё плохо и это ТЕСТ - всё равно шлем смс
    if last_version == "TEST":
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                     json={"chat_id": CHAT_ID, "text": "Бот вообще ничего не видит!"})
