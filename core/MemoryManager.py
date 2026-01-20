from langchain_core.messages import BaseMessage

class MemoryManager:
    """Класс для управления историей диалога."""
    
    def __init__(self):
        # Храним историю как список объектов сообщений
        self.history: list[BaseMessage] = []

    def get_history(self) -> list[BaseMessage]:
        """Возвращает всю историю сообщений."""
        return self.history

    def add_messages(self, messages: list[BaseMessage]):
        """Добавляет новые сообщения в историю."""
        self.history.extend(messages)

    def clear(self):
        """Очищает историю."""
        self.history = []