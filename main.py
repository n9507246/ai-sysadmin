from YandexGPT import YandexGPT
import config 

def main():


    print("AI-ассистент запущен. Введите 'exit' для выхода.")
    while True:
        user_input = input("\nВы: ")
        if user_input.lower() in ("exit", "quit"):
            break

        result = YandexGPT().ask([
            { "role": "system", "content": config.SYSTEM_PROMPT}, # установка роли системы(БЕЗ НЕГО МОДЕЛЬ НЕ РАБОТАЕТ)
            { "role": "user",  "content": user_input} # вопрос пользователя
        ])

        print(f"\nAI: {result}")

       


if __name__ == "__main__":
    main()