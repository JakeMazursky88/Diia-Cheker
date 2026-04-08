import requests
import os
import time
import re
import urllib.parse

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"

# Основные источники
URL_API = f"https://itunes.apple.com/ua/lookup?id={APP_ID}&t={int(time.time())}"
URL_WEB = f"https://apps.apple.com/ua/app/id{APP_ID}"
# Прокси-сервис для обхода бана по IP
PROXY_URL = f"https://api.allorigins.win/raw?url={urllib.parse.quote(URL_API)}"

file_path = "version.txt"

def send_full_alert(ver):
    print(f"!!! НАШЕЛ ВЕРСИЮ: {ver}. ШЛЮ 10 СМС !!!")
    for i in range(1, 11):
        text = f"🚨 ВЛАД, ПОДЪЕМ! ДІЯ {ver}! 🚨\n(Сигнал {i}/10)"
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                         json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        except: pass
        time.sleep(6) # Ровно 1 минута вибрации
    with open(file_path, "w") as f:
        f.write(ver)

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

print(f"--- СТАРТ ПРОВЕРКИ (В файле: {last_version}) ---")
current_version = None

try:
    # ПОПЫТКА 1: Прокси (обход бана IP)
    print("Пробую через прокси...")
    res = requests.get(PROXY_URL, timeout=20).json()
    if res.get('resultCount', 0) > 0:
        current_version = str(res['results'][0]['version']).strip()
        print(f"✅ Прокси сработал! Версия: {current_version}")
except:
    print("Прокси не помог.")

if not current_version:
    try:
        # ПОПЫТКА 2: Прямой API с маскировкой
        print("Пробую прямой API...")
        h = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(URL_API, headers=h, timeout=15).json()
        if res.get('resultCount', 0) > 0:
            current_version = str(res['results'][0]['version']).strip()
            print(f"✅ Прямой API ожил! Версия: {current_version}")
    except:
        print("Прямой API всё еще в бане.")

if not current_version:
    try:
        # ПОПЫТКА 3: Брутфорс поиск в коде страницы
        print("Ищу в коде страницы...")
        res = requests.get(URL_WEB, headers={'User-Agent': 'Mozilla/5.0'}, timeout=20).text
        # Ищем любую комбинацию цифр после слова version
        match = re.search(r'\"version\":\"([\d\.]+)\"', res)
        if match:
            current_version = match.group(1).strip()
            print(f"✅ Нашел в коде! Версия: {current_version}")
    except:
        print("В коде страницы пусто.")

# ИТОГОВЫЙ РЕЗУЛЬТАТ
if current_version:
    if current_version != last_version or last_version == "1":
        send_full_alert(current_version)
    else:
        print("Обновлений нет, версии совпали.")
else:
    print("❌ НИ ОДИН СПОСОБ НЕ СРАБОТАЛ.")
    if last_version == "1":
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                     json={"chat_id": CHAT_ID, "text": "⚠️ ВСЕ МЕТОДЫ СДОХЛИ. Apple заблокировала даже прокси."})
