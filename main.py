from YandexGPT import YandexGPT
import config 

def main():

    user_input = "Когда родился Александр Сергеевич Пушкин?"

    print(
        YandexGPT().ask([
            { "role": "system", "content": config.SYSTEM_PROMPT}, # установка роли системы(БЕЗ НЕГО МОДЕЛЬ НЕ РАБОТАЕТ)
            { "role": "user",  "content": user_input} # вопрос пользователя
        ]))



if __name__ == "__main__":
    main()