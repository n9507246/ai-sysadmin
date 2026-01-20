import json
import os
# Используем базовые классы сообщений для типизации и логики
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

class MemoryManager:
    """
    Менеджер памяти, реализующий механизм 'скользящего окна'.
    Хранит только последние N сообщений, чтобы контекст не разрастался бесконечно.
    """

    def __init__(self, file_path: str = "history.json", max_entries: int = 20):
        """
        :param file_path: Путь к файлу для постоянного хранения.
        :param max_entries: Лимит сообщений в памяти (например, 20 сообщений = 10 диалогов).
        """
        self.file_path = file_path
        self.max_entries = max_entries
        # При загрузке сразу получаем актуальную историю, не превышающую лимит
        self.history: list[BaseMessage] = self._load_from_file()

    def _load_from_file(self) -> list[BaseMessage]:
        """
        Загружает историю из JSON и восстанавливает объекты сообщений.
        """
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                messages = []
                for item in data:
                    # Восстанавливаем типы сообщений на основе сохраненного поля 'type'
                    if item["type"] == "human":
                        messages.append(HumanMessage(content=item["content"]))
                    elif item["type"] == "ai":
                        messages.append(AIMessage(content=item["content"]))
                
                # Слайсинг [-max_entries:]: берем только последние элементы списка.
                # Это гарантирует соблюдение лимита, даже если JSON редактировали вручную.
                return messages[-self.max_entries:]
        except Exception as e:
            print(f"Ошибка при загрузке истории: {e}")
            return []

    def save_to_file(self):
        """
        Метод автоматической обрезки и сохранения истории в файл.
        """
        try:
            # 1. Проверяем текущий размер истории.
            # Если сообщений больше лимита, отсекаем самые старые (из начала списка).
            if len(self.history) > self.max_entries:
                self.history = self.history[-self.max_entries:]

            # 2. Конвертируем объекты в компактный формат (тип + текст)
            compact_data = []
            for msg in self.history:
                msg_type = "human" if isinstance(msg, HumanMessage) else "ai"
                compact_data.append({
                    "type": msg_type,
                    "content": msg.content
                })

            # 3. Перезаписываем файл актуальными данными
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(compact_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении истории: {e}")

    def get_history(self) -> list[BaseMessage]:
        """Возвращает историю для передачи в LangGraph Agent."""
        return self.history

    def add_messages(self, messages: list[BaseMessage]):
        """
        Добавляет новую порцию сообщений в конец истории и инициирует сохранение.
        """
        self.history.extend(messages)
        # Вызов сохранения также спровоцирует проверку лимита (обрезку)
        self.save_to_file()

    def clear(self):
        """
        Метод для полной очистки диалога. Удаляет файл и обнуляет историю в памяти.
        """
        self.history = []
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        print("История переписки полностью очищена.")