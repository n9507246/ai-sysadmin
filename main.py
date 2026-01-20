from agent.my_agent.Agent import Agent
from core.MemoryManager import MemoryManager

def main():

    # Создаем агента
    agent = Agent()
    memory = MemoryManager() # Инициализируем память
    
    print("AI-ассистент запущен. Введите 'exit' для выхода.")
    
    # Основной цикл взаимодействия с пользователем
    while True:
        # Получаем ввод от пользователя
        user_input = input("\nВы: ")
        # если пользователь ввел 'exit', заканчиваем работу
        if user_input.lower() in ("exit", "quit"):
            break
        else:
            # Запускаем агента с пользовательским вводом и историей из памяти 
            result = agent.run(user_input, history=memory.get_history())
            
            # Обновляем память новыми сообщениями из результата
            # Берем последние два (Human и AI)
            memory.add_messages(result["messages"][-2:])

        # после того, как агент отработал, он 
        # возвращает состояние AgentState 
        # выводим поле output
        print(f"\nAI: {result['output']}")

       


if __name__ == "__main__":
    main()