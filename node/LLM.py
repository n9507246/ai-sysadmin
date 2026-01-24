import uuid
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

class LLM:
    def __init__(self, model, system_prompt):
        self.model = model
        self.system_prompt = system_prompt

    def __call__(self, state: dict) -> dict:
        summary = state.get("summary", "")
        
        current_system_prompt = self.system_prompt
        if summary:
            current_system_prompt += f"\nКраткое содержание предыдущей беседы: {summary}"
        
        messages = [
            SystemMessage(content=current_system_prompt),
            *state.get("messages", [])
        ]
        
        response_text = self.model.ask(messages)
        
        # Генерируем ID для новой пары сообщений
        return {
            "output": response_text,
            "messages": [
                AIMessage(content=response_text, id=str(uuid.uuid4()))
            ]
        }