import requests
import os
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"

# Используем только украинский регион, но с жесткой маскировкой
URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua&entity=software"

file_path = "version.txt"

print("--- ЗАПУСК ПРОВЕРКИ ---")

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

try:
    # Имитируем реальный iPhone, который заходит в магазин
    headers = {
        'User-Agent': 'AppStore/3.0 iOS/15.0 model/iPhone13,2 build/19A346 (6; dt:209)',
        'X-Apple-Store-Front': '143465-1,29' # Код украинского стора
    }
    
    response = requests.get(URL, headers=headers, timeout=20).json()
    
    if response.get('resultCount', 0) > 0:
        current_version = str(response['results'][0]['version']).strip()
        print(f"✅ УСПЕХ! Версия в UA Store: {current_version}")
        
        # СРАВНЕНИЕ (или принудительный тест через TEST в файле)
        if current_version != last_version or last_version == "TEST":
            print(f"!!! ЕСТЬ ОБНОВА: {last_version} -> {current_version} !!!")
            
            # 10 уведомлений (1 минута вибрации)
            for i in range(1, 11):
                msg = f"🚨 ВЛАД, ПОДЪЕМ! ДІЯ ОБНОВИЛАСЬ! 🚨\nВерсия: {current_version}\n(Сигнал {i}/10)"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             json={"chat_id": CHAT_ID, "text": msg})
                time.sleep(6)
            
            # Сохраняем новую версию, если это не тест
            if last_version != "TEST":
                with open(file_path, "w") as f:
                    f.write(current_version)
        else:
            print("Версии совпадают. Спим.")
            
    else:
        print("❌ App Store снова прислал пустой список. Apple блокирует сервер Гитхаба.")
        # Если пусто — шлем ТЕБЕ одно смс, что бот ослеп (чтобы ты знал, что надо проверить вручную)
        if last_version == "TEST":
             requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          json={"chat_id": CHAT_ID, "text": "⚠️ Бот не видит App Store! Apple блокирует запросы."})

except Exception as e:
    print(f"Ошибка: {e}")
