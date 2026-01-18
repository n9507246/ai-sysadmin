import config 
from agent.my_agent.Agent import Agent
def main():

    # Создаем агента
    agent = Agent()

    print("AI-ассистент запущен. Введите 'exit' для выхода.")
    
    # Основной цикл взаимодействия с пользователем
    while True:
        # Получаем ввод от пользователя
        user_input = input("\nВы: ")
        # если пользователь ввел 'exit', заканчиваем работу
        if user_input.lower() in ("exit", "quit"):
            break
        else:
            # Запускаем агента с пользовательским вводом
            result = agent.run(user_input)

        # после того, как агент отработал, он 
        # возвращает состояние AgentState 
        # выводим поле output
        print(f"\nAI: {result['output']}")

       


if __name__ == "__main__":
    main()