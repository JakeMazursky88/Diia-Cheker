import requests
import os
import time

# Подтягиваем секреты из настроек GitHub
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"
URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua"

file_path = "version.txt"

# 1. Читаем версию из файла
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

print(f"--- ПРОВЕРКА ---")
print(f"В файле: '{last_version}'")

try:
    # 2. Стучимся в App Store
    response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15).json()
    
    if response.get('resultCount', 0) > 0:
        current_version = str(response['results'][0]['version']).strip()
        print(f"В магазине: '{current_version}'")
        
        # 3. СРАВНЕНИЕ (Если не совпало — поднимаем тревогу)
        if current_version != last_version:
            print("!!! ВНИМАНИЕ: ВЕРСИИ НЕ СОВПАДАЮТ, ШЛЮ СПАМ !!!")
            
            # Цикл на 1 минуту (20 сообщений по 3 сек)
            for i in range(20):
                text = f"🚨 ВЛАД, ПОДЪЕМ!!! ДІЯ ОБНОВИЛАСЬ! 🚨\nВерсия: {current_version}\n(Сигнал {i+1}/20)"
                
                # Отправка и проверка ответа от Телеграма
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                     json={"chat_id": CHAT_ID, "text": text})
                
                if res.status_code != 200:
                    print(f"ОШИБКА ТЕЛЕГРАМА: {res.status_code} - {res.text}")
                else:
                    print(f"Сообщение {i+1} ушло успешно!")
                
                time.sleep(3) 
            
            # Сохраняем новую версию только если всё прошло успешно
            with open(file_path, "w") as f:
                f.write(current_version)
        else:
            print("Обновлений нет, версии одинаковые.")
    else:
        print("Ошибка: Не удалось получить данные из App Store.")

except Exception as e:
    print(f"Критическая ошибка скрипта: {e}")
