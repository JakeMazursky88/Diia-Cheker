import requests
import os
import time

# Данные из секретов
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"
URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua"

file_path = "version.txt"

print("--- ШАГ 1: ЗАПУСК СКРИПТА ---")

# 1. Читаем старую версию
try:
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            last_version = f.read().strip()
    else:
        last_version = "0"
    print(f"Старая версия из файла: '{last_version}'")
except Exception as e:
    print(f"Ошибка при чтении файла: {e}")
    last_version = "0"

# 2. Получаем версию из App Store
try:
    print("Запрашиваю данные из App Store...")
    resp = requests.get(URL, timeout=15).json()
    current_version = str(resp['results'][0]['version']).strip()
    print(f"Текущая версия в магазине: '{current_version}'")
except Exception as e:
    print(f"Не удалось получить версию из магазина: {e}")
    current_version = last_version # Чтобы не сработал ложный сигнал

# 3. СРАВНЕНИЕ И ОТПРАВКА
# Если версии не равны ИЛИ в файле написано TEST
if current_version != last_version or last_version == "TEST":
    print(f"!!! РАЗНИЦА НАЙДЕНА: {last_version} -> {current_version} !!!")
    print("Начинаю отправку 10 сообщений...")
    
    for i in range(1, 11):
        text = f"🚨 ВЛАД, ПОДЪЕМ! ДІЯ ОБНОВИЛАСЬ! 🚨\nВерсия: {current_version}\n(Сигнал {i}/10)"
        
        try:
            r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             json={"chat_id": CHAT_ID, "text": text}, timeout=10)
            if r.status_code == 200:
                print(f"[{i}/10] СМС ушло успешно")
            else:
                print(f"[{i}/10] Ошибка отправки: {r.status_code} - {r.text}")
        except Exception as e:
            print(f"[{i}/10] Ошибка соединения: {e}")
        
        # Пауза 6 секунд между сообщениями (ровно 1 минута на всё)
        time.sleep(6)

    # Сохраняем версию только если это не был ручной TEST
    if last_version != "TEST":
        with open(file_path, "w") as f:
            f.write(current_version)
        print("Версия обновлена в файле.")
else:
    print("Версии совпадают. Ничего не шлю.")

print("--- ШАГ 2: СКРИПТ ЗАВЕРШЕН ---")
