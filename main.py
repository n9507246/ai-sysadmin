from YandexGPT import YandexGPT


def main():
   
    SYSTEM_PROMPT = "You are a helpful assistant." 
    user_input = "Когда родился Александр Сергеевич Пушкин?"

    print(
        YandexGPT().ask([
            { "role": "system", "content": SYSTEM_PROMPT}, # установка роли системы(БЕЗ НЕГО МОДЕЛЬ НЕ РАБОТАЕТ)
            { "role": "user",  "content": user_input} # вопрос пользователя
        ]))

if __name__ == "__main__":
    main()