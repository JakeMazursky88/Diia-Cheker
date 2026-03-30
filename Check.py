import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = [id for id in [os.getenv("TELEGRAM_CHAT_ID"), os.getenv("FRIEND_CHAT_ID")] if id]

# ID из твоего скрина (основная Дия)
APP_ID = "1483089069"
# Универсальная ссылка без привязки к стране
URL = f"https://itunes.apple.com/lookup?id={APP_ID}"

file_path = os.path.join(os.getcwd(), "version.txt")

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

print(f"Запрос к Apple по ID: {APP_ID}...")

try:
    response = requests.get(URL, timeout=15).json()
    
    if response.get('resultCount', 0) > 0:
        current_version = response['results'][0]['version']
        print(f"Версия в магазине: {current_version}")
        
        if str(current_version) != str(last_version):
            msg = f"🚀 Обновление Дії!\nНовая версия: {current_version}\n(В файле была: {last_version})"
            
            for chat_id in CHAT_IDS:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             json={"chat_id": chat_id, "text": msg})
            
            with open(file_path, "w") as f:
                f.write(str(current_version))
            print("✅ СМС отправлено, версия обновлена.")
        else:
            print(f"Версия совпадает ({current_version}), отправка не нужна.")
    else:
        # Если поиск по ID не дал результата, попробуем через прямой поиск по имени
        print("По ID не нашли, пробую поиск по имени 'Diia'...")
        search_url = "https://itunes.apple.com/search?term=Diia&country=ua&entity=software"
        search_res = requests.get(search_url).json()
        if search_res.get('resultCount', 0) > 0:
            # Берем первый результат поиска
            current_version = search_res['results'][0]['version']
            print(f"Найдено через поиск. Версия: {current_version}")
            # ... тут дублируем логику сравнения и отправки ...
            if str(current_version) != str(last_version):
                msg = f"🚀 Обновление Дії!\nВерсия: {current_version}"
                for chat_id in CHAT_IDS:
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": chat_id, "text": msg})
                with open(file_path, "w") as f:
                    f.write(str(current_version))
        else:
            print("❌ Приложение не найдено даже через поиск.")

except Exception as e:
    print(f"❌ Ошибка: {e}")
