import requests
import os
import time
import re

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"
# Страница в браузере, её Apple отдает охотнее, чем API
URL = f"https://apps.apple.com/ua/app/id{APP_ID}"

file_path = "version.txt"

def send_notifications(version):
    print(f"Запускаю серию уведомлений для версии {version}...")
    # 7 сообщений — это золотая середина (и разбудит, и не забанят)
    for i in range(1, 8):
        text = f"🚨 ВЛАД, ПОДЪЕМ! ДІЯ ОБНОВИЛАСЬ! 🚨\nВерсия: {version}\n(Сигнал {i} из 7)"
        try:
            r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             json={"chat_id": CHAT_ID, "text": text}, timeout=10)
            if r.status_code == 429: # Если вдруг словили ограничение
                wait_time = r.json().get('parameters', {}).get('retry_after', 10)
                time.sleep(wait_time)
            print(f"Отправлено {i}/7. Статус: {r.status_code}")
        except Exception as e:
            print(f"Ошибка отправки: {e}")
        
        # Пауза 8 секунд — iPhone успеет провибрировать, а Telegram не забанит
        time.sleep(8)

# 1. Читаем старую версию
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

try:
    # 2. Идем на страницу как обычный браузер
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(URL, headers=headers, timeout=20)
    
    # 3. Ищем версию в коде страницы
    # Регулярка ищет паттерн "version":"X.X.X"
    version_match = re.search(r'\"version\":\"([^\"]+)\"', response.text)
    
    if version_match:
        current_version = version_match.group(1).strip()
        print(f"Нашел версию: {current_version} (в файле было: {last_version})")
        
        # 4. СРАВНИВАЕМ
        if current_version != last_version or last_version == "TEST":
            send_notifications(current_version)
            
            # Сохраняем новую версию (только если это не принудительный ТЕСТ)
            if last_version != "TEST":
                with open(file_path, "w") as f:
                    f.write(current_version)
        else:
            print("Обновлений нет.")
    else:
        print("Не удалось найти версию на странице. Возможно, Apple поменяла дизайн кода.")
        if last_version == "TEST":
             requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          json={"chat_id": CHAT_ID, "text": "⚠️ Бот не видит версию на сайте!"})

except Exception as e:
    print(f"Ошибка: {e}")
