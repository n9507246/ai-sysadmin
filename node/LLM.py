from utils.YandexGPT import YandexGPT
from config import SYSTEM_PROMPT
from agent.my_agent.AgentState import AgentState

class LLM():
    '''Узел для взаимодействия с LLM-моделью.'''

    def __init__(self):
        self.model = YandexGPT()  # Передаем класс модели и создаем его экземпляр
        self.system_prompt = SYSTEM_PROMPT # Системный промпт для модели

    def __call__( self, state: AgentState ) -> dict: 
        
        
        user_input = state.get("input") # Получаем пользовательский ввод из состояния

        messages = [{"role": "system", "content": self.system_prompt}]  # Инициализируем сообщения с системным промптом
        messages.append({"role": "user", "content": user_input})  # Добавляем пользовательское сообщение
        response = self.model.ask(messages) # Отправляем запрос модели и получаем ответ
        return {"output": response} # Возвращаем обновленное состояние с ответом модели