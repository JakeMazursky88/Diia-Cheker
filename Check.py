import requests
import os

# Подтягиваем ключи из настроек (Secrets)
TOKEN = os.getenv("TELEGRAM_TOKEN")
# Список ID: твой и друга (если есть)
CHAT_IDS = [os.getenv("TELEGRAM_CHAT_ID"), os.getenv("FRIEND_CHAT_ID")]

# ID Дии в App Store
APP_ID = "1489715534"
URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua"

# 1. Читаем прошлую версию из файла
try:
    with open("version.txt", "r") as f:
        last_version = f.read().strip()
except FileNotFoundError:
    last_version = ""

# 2. Проверяем текущую версию в App Store
try:
    response = requests.get(URL, timeout=10).json()
    if response.get('resultCount', 0) > 0:
        current_version = response['results'][0]['version']
        print(f"Проверка: версия в App Store — {current_version}, была — {last_version}")

        # 3. Если версия новая или это первый запуск
        if current_version != last_version:
            msg = f"🚀 Внимание! Вышло обновление Дії!\nНовая версия: {current_version}\n\nПроверь App Store прямо сейчас."
            
            for chat_id in CHAT_IDS:
                if chat_id: # Отправляем только если ID прописан в секретах
                    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    requests.post(api_url, json={"chat_id": chat_id, "text": msg})
            
            # 4. Записываем новую версию в файл
            with open("version.txt", "w") as f:
                f.write(current_version)
    else:
        print("Ошибка: Приложение не найдено в App Store.")

except Exception as e:
    print(f"Произошла ошибка: {e}")

