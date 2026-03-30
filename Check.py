import requests
import os

# Берем данные из секретов GitHub
TOKEN = os.getenv("TELEGRAM_TOKEN")
# Список ID (твой и друга). Скрипт проигнорирует пустые, если FRIEND_CHAT_ID не задан.
CHAT_IDS = [id for id in [os.getenv("TELEGRAM_CHAT_ID"), os.getenv("FRIEND_CHAT_ID")] if id]

# ПРАВИЛЬНЫЙ ID приложения Дія (из твоего скриншота)
APP_ID = "1483089069"
URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua"

# Определяем путь к файлу с версией в системе GitHub
file_path = os.path.join(os.getcwd(), "version.txt")

# 1. Читаем старую версию из файла
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

print(f"Проверка версии... (Текущая в файле: {last_version})")

try:
    # 2. Запрашиваем данные у Apple
    response = requests.get(URL, timeout=15).json()
    
    if response.get('resultCount', 0) > 0:
        current_version = response['results'][0]['version']
        print(f"Версия в App Store: {current_version}")
        
        # 3. Сравниваем
        if str(current_version) != str(last_version):
            print("Найдено отличие! Отправляю уведомления...")
            msg = f"🚀 Обновление Дії!\nНовая версия в App Store: {current_version}\n(Была: {last_version})"
            
            # Рассылка всем указанным ID
            for chat_id in CHAT_IDS:
                send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                res = requests.post(send_url, json={"chat_id": chat_id, "text": msg})
                
                if res.status_code == 200:
                    print(f"✅ Сообщение отправлено в чат {chat_id}")
                else:
                    print(f"❌ Ошибка отправки в {chat_id}: {res.text}")
            
            # 4. Обновляем файл только если хоть одно сообщение ушло успешно
            with open(file_path, "w") as f:
                f.write(str(current_version))
            print("Файл version.txt обновлен.")
            
        else:
            print("Изменений нет. Спим дальше.")
    else:
        print("Ошибка: Не удалось найти приложение в App Store. Проверь APP_ID.")

except Exception as e:
    print(f"❌ Критическая ошибка в скрипте: {e}")
