import requests
import os
import time
import re

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Канал 1: Через bundleId (другой путь в базе Apple)
URL_BUNDLE = "https://itunes.apple.com/lookup?bundleId=ua.gov.diia.app&country=ua"
# Канал 2: Сторонний сайт-агрегатор
URL_AGGREGATOR = "https://www.iosnoops.com/appinfo/diia-for-iphone/"

file_path = "version.txt"

def send_attack(ver):
    print(f"!!! ЕСТЬ ПРОБИТИЕ! ВЕРСИЯ: {ver} !!!")
    for i in range(1, 11):
        text = f"🚨 ВЛАД, ПОДЪЕМ! ДІЯ {ver}! 🚨\nСигнал {i}/10 — ОДЕССА ЖДЕТ!"
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                         json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        except: pass
        time.sleep(7) # ~70 секунд непрерывной долбежки
    with open(file_path, "w") as f:
        f.write(ver)

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

print(f"--- РАБОТАЕМ. В файле: {last_version} ---")
current_version = None

# ШАГ 1: Пробуем Канал 1 (Bundle ID)
try:
    print("Пробую Bundle ID...")
    # Добавляем случайный параметр, чтобы Apple не подсовывала кэш
    res = requests.get(f"{URL_BUNDLE}&t={int(time.time())}", timeout=15).json()
    if res.get('resultCount', 0) > 0:
        current_version = str(res['results'][0]['version']).strip()
        print(f"✅ Канал 1 выдал: {current_version}")
except:
    print("Канал 1 в бане.")

# ШАГ 2: Если первый сдох, пробуем Канал 2 (Агрегатор)
if not current_version:
    try:
        print("Пробую Агрегатор iOSNoops...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(URL_AGGREGATOR, headers=headers, timeout=20).text
        # Ищем версию в тексте страницы (обычно там "Current Version: X.X.X")
        match = re.search(r'Version:\s*([\d\.]+)', res)
        if match:
            current_version = match.group(1).strip()
            print(f"✅ Канал 2 выдал: {current_version}")
    except:
        print("Канал 2 тоже лежит.")

# ИТОГ
if current_version:
    # Убираем всё, кроме цифр и точек на всякий случай
    current_version = "".join(c for c in current_version if c.isdigit() or c == '.')
    
    if current_version != last_version or last_version == "1":
        send_attack(current_version)
    else:
        print("Версии совпали. Пока тихо.")
else:
    print("❌ ТОТАЛЬНЫЙ БАН. Apple перекрыла всё.")
    if last_version == "1":
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                     json={"chat_id": CHAT_ID, "text": "⚠️ ТРЕВОГА! Бот полностью ослеп, Apple заблокировала все каналы!"})
