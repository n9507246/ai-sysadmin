from agent.my_agent.Agent import Agent
from core.MemoryManager import MemoryManager
from config import HISTORY_MAX_ENTRIES


def main():

    # Настройки здесь:
    THRESHOLD = 20    # Суммаризировать, когда накопится 20 сообщений
    KEEP = 10         # После суммаризации оставлять 10 последних "живых" сообщений
    FILE_LIMIT = 40   # Максимальный размер файла (страховка)

    agent = Agent(summary_threshold=THRESHOLD, keep_messages=KEEP)
    memory = MemoryManager("history.json", max_entries=FILE_LIMIT)
    
    print(f"Запущено: Порог={THRESHOLD}, Оставляем={KEEP}")
    
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