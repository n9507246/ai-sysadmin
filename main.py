from agent.my_agent.Agent import Agent
from core.MemoryManager import MemoryManager
from config import HISTORY_MAX_ENTRIES, SUMMARY_THRESHOLD, KEEP_MESSAGES


def main():

    agent = Agent(summary_threshold=SUMMARY_THRESHOLD, keep_messages=KEEP_MESSAGES)
    memory = MemoryManager("history.json", max_entries=HISTORY_MAX_ENTRIES)
    
    print(f"Запущено: Порог={SUMMARY_THRESHOLD}, Оставляем={KEEP_MESSAGES}")
    
    # Основной цикл взаимодействия с пользователем
    while True:
        # Получаем ввод от пользователя
        user_input = input("\nВы: ")
        # если пользователь ввел 'exit', заканчиваем работу
        if user_input.lower() in ("exit", "quit"):
            break
        else:
            # 1. Запуск агента
            result = agent.run(
                user_input, 
                history=memory.get_history(),
                summary=memory.get_summary()
            )

            # ПОСЛЕ выполнения графа в result["messages"] будут 
            # только те сообщения, которые выжили после удаления
            updated_messages = result.get("messages", [])
            updated_summary = result.get("summary") or memory.get_summary()

            # Синхронизируем физический файл с отфильтрованным списком
            memory.add_messages(updated_messages, summary=updated_summary)

        # после того, как агент отработал, он 
        # возвращает состояние AgentState 
        # выводим поле output
        print(f"\nAI: {result['output']}")

       


if __name__ == "__main__":
    main()