import json
import os
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, messages_from_dict, messages_to_dict

class MemoryManager:
    """
    Класс для управления долгосрочной памятью агента.
    Сохраняет историю сообщений в JSON-файл и загружает её при старте.
    """

    def __init__(self, file_path: str = "chat_history.json"):
        self.file_path = file_path
        self.history: list[BaseMessage] = self._load_from_file()

    def _load_from_file(self) -> list[BaseMessage]:
        """Загружает историю из файла и конвертирует её в объекты сообщений."""
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # messages_from_dict — встроенная функция LangChain, 
                # которая превращает JSON-структуру обратно в объекты HumanMessage/AIMessage
                return messages_from_dict(data)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Ошибка при загрузке истории: {e}")
            return []

    def save_to_file(self):
        """Конвертирует объекты сообщений в JSON и сохраняет на диск."""
        try:
            # messages_to_dict превращает объекты сообщений в список словарей
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(messages_to_dict(self.history), f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении истории: {e}")

    def get_history(self) -> list[BaseMessage]:
        """Возвращает текущую историю сообщений."""
        return self.history

    def add_messages(self, messages: list[BaseMessage]):
        """Добавляет новые сообщения в историю и сразу сохраняет их в файл."""
        self.history.extend(messages)
        self.save_to_file()

    def clear(self):
        """Полностью очищает историю и удаляет файл."""
        self.history = []
        if os.path.exists(self.file_path):
            os.remove(self.file_path)