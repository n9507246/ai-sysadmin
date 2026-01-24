import json
import os
import uuid
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

class MemoryManager:
    def __init__(self, file_path: str = "history.json", max_entries: int = 30):
        self.file_path = file_path
        self.max_entries = max_entries
        self.current_summary = ""
        self.history: list[BaseMessage] = self._load_from_file()

    def _load_from_file(self) -> list[BaseMessage]:
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.current_summary = data.get("summary", "")
                messages = []
                for item in data.get("messages", []):
                    # Загружаем ID или генерируем новый, если его нет
                    m_id = item.get("id", str(uuid.uuid4()))
                    if item["type"] == "human":
                        messages.append(HumanMessage(content=item["content"], id=m_id))
                    elif item["type"] == "ai":
                        messages.append(AIMessage(content=item["content"], id=m_id))
                return messages[-self.max_entries:]
        except Exception as e:
            print(f"[ERROR] Ошибка загрузки: {e}")
            return []

    def save_to_file(self, summary: str = None):
        try:
            if summary:
                self.current_summary = summary
            
            save_data = {
                "summary": self.current_summary,
                "messages": [
                    {
                        "type": "human" if isinstance(m, HumanMessage) else "ai",
                        "content": m.content,
                        "id": m.id # Сохраняем ID для синхронизации с графом
                    } for m in self.history
                ]
            }
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(save_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[ERROR] Ошибка сохранения: {e}")

    def add_messages(self, all_messages: list[BaseMessage], summary: str = None):
        # Гарантируем, что у всех сообщений есть ID
        for m in all_messages:
            if not m.id:
                m.id = str(uuid.uuid4())
        self.history = all_messages
        self.save_to_file(summary=summary)

    def get_history(self): return self.history
    def get_summary(self): return self.current_summary