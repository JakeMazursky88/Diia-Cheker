        if str(current_version) != str(last_version):
            print(f"!!! НАШЕЛ ОБНОВЛЕНИЕ: {current_version} !!!")
            
            # ЦИКЛ "БЕШЕНОЕ УВЕДОМЛЕНИЕ"
            # Отправим 50 штук, чтобы телефон не замолкал очень долго
            for i in range(50):
                text = f"🚨 ВЛАД, ПОДЪЕМ!!! ДІЯ ОБНОВИЛАСЬ! 🚨\nВерсия: {current_version}\nБЕГОМ ЗА КВАРТИРОЙ! (Сигнал {i+1}/50)"
                
                # Шлем в твой основной бот
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             json={"chat_id": CHAT_ID, "text": text})
                
                # Пауза 2 секунды, чтобы вибрация успела протрясти телефон
                time.sleep(2) 
            
            # Сохраняем новую версию в файл только ПОСЛЕ того, как отправили весь спам
            with open(file_path, "w") as f:
                f.write(str(current_version))
