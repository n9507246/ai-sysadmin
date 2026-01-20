from agent.my_agent.Agent import Agent
from core.MemoryManager import MemoryManager

def main():

    # Инициализируем агента и память
    agent = Agent()
    memory = MemoryManager("history.json", max_entries=10)
    
    print("AI-ассистент запущен. Введите 'exit' для выхода.")
    
    # Основной цикл взаимодействия с пользователем
    while True:
        # Получаем ввод от пользователя
        user_input = input("\nВы: ")
        # если пользователь ввел 'exit', заканчиваем работу
        if user_input.lower() in ("exit", "quit"):
            break
        else:
            # 1. Запускаем агента, передавая историю из памяти
            result = agent.run(user_input, history=memory.get_history())
            
            # 2. Извлекаем последние два сообщения (HumanMessage и AIMessage)
            # Они уже добавлены в state графом LangGraph внутри Agent.run
            if "messages" in result and len(result["messages"]) >= 2:
                new_chat_step = result["messages"][-2:]
                
                # 3. Добавляем их в память ОДИН РАЗ
                # Этот метод сам вызовет save_to_file()
                memory.add_messages(new_chat_step)

        # после того, как агент отработал, он 
        # возвращает состояние AgentState 
        # выводим поле output
        print(f"\nAI: {result['output']}")

       


if __name__ == "__main__":
    main()