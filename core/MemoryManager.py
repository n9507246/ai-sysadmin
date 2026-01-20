import json
import os
# Импортируем только необходимые базовые классы сообщений
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

class MemoryManager:
    """
    Класс для управления историей диалога. 
    Обеспечивает компактное хранение данных в JSON, оставляя только тип сообщения и его текст.
    """

    def __init__(self, file_path: str = "history.json"):
        """
        Инициализация менеджера памяти.
        :param file_path: Путь к файлу, в котором будет храниться история.
        """
        self.file_path = file_path
        # При создании экземпляра сразу пытаемся загрузить существующую историю из файла
        self.history: list[BaseMessage] = self._load_from_file()

    def _load_from_file(self) -> list[BaseMessage]:
        """
        Загружает данные из JSON-файла и восстанавливает их в объекты LangChain.
        Это необходимо, так как LangGraph и LLM-узлы ожидают объекты классов, а не просто словари.
        """
        # Если файла еще нет (первый запуск), возвращаем пустой список
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                messages = []
                # Проходим по каждому упрощенному словарю в JSON
                for item in data:
                    # На основе строкового значения "type" создаем соответствующий объект класса
                    if item["type"] == "human":
                        messages.append(HumanMessage(content=item["content"]))
                    elif item["type"] == "ai":
                        messages.append(AIMessage(content=item["content"]))
                return messages
        except Exception as e:
            # Если файл поврежден или возникла ошибка чтения, выводим её и возвращаем пустой список
            print(f"Ошибка при загрузке истории: {e}")
            return []

    def save_to_file(self):
        """
        Конвертирует текущий список объектов BaseMessage в упрощенный формат JSON.
        Мы сознательно игнорируем ID сообщений и прочие метаданные для чистоты файла.
        """
        try:
            compact_data = []
            # Перебираем все сообщения в текущей сессии
            for msg in self.history:
                # Проверяем экземпляр класса, чтобы определить строковую метку роли
                if isinstance(msg, HumanMessage):
                    msg_type = "human"
                elif isinstance(msg, AIMessage):
                    msg_type = "ai"
                else:
                    msg_type = "human" # Резервный тип

                # Формируем минималистичный словарь для записи
                compact_data.append({
                    "type": msg_type,
                    "content": msg.content
                })

            # Записываем список словарей в файл с отступами для читаемости
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(compact_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении истории: {e}")

    def get_history(self) -> list[BaseMessage]:
        """Возвращает текущий список сообщений в виде объектов для передачи в Agent."""
        return self.history

    def add_messages(self, messages: list[BaseMessage]):
        """
        Добавляет новые сообщения в память и синхронизирует изменения с файлом на диске.
        :param messages: Список новых сообщений (обычно пара: HumanMessage и AIMessage).
        """
        self.history.extend(messages)
        # Автоматическое сохранение после каждого обновления, чтобы не потерять данные при сбое
        self.save_to_file()