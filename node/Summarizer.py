from agent.my_agent.AgentState import AgentState
from langchain_core.messages import RemoveMessage

class Summarizer:
    def __init__(self, model, instruction, summary_threshold: int = 16, keep_messages: int = 6):
        """
        :param summary_threshold: Когда запускать суммаризацию.
        :param keep_messages: Сколько последних сообщений НЕ удалять.
        """
        self.model = model
        self.instruction = instruction
        self.summary_threshold = summary_threshold
        self.keep_messages = keep_messages

    def __call__(self, state: AgentState):
        messages = state.get("messages", [])
        print(f"[LOG] Сообщений в памяти: {len(messages)}")

        if len(messages) < self.summary_threshold:
            return {} 

        print(f"[LOG] Порог ({self.summary_threshold}) превышен. Суммаризация...")
        
        history_text = "\n".join([f"{m.type}: {m.content}" for m in messages])
        prompt = [
            {"role": "system", "content": self.instruction},
            {"role": "user", "content": f"Суммаризируй это:\n{history_text}"}
        ]
        
        try:
            summary = self.model.ask(prompt)
            # Удаляем все сообщения, кроме последних self.keep_messages
            delete_messages = [RemoveMessage(id=m.id) for m in messages[:-self.keep_messages] if m.id]
            
            return {
                "summary": summary, 
                "messages": delete_messages 
            }
        except Exception as e:
            print(f"[ERROR] Ошибка суммаризации: {e}")
            return {}