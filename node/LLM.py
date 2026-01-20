from utils.YandexGPT import YandexGPT
from config import SYSTEM_PROMPT
from agent.my_agent.AgentState import AgentState
# Импортируем классы сообщений, которые LangGraph будет использовать в состоянии
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

class LLM():
    '''
    Узел графа (Node), отвечающий за логику взаимодействия с нейросетью.
    Этот класс вызывается LangGraph как функция на определенном этапе работы агента.
    '''

    def __init__(self):
        # Инициализируем наш адаптер для YandexGPT
        self.model = YandexGPT()  
        # Загружаем общие инструкции для поведения модели из конфига
        self.system_prompt = SYSTEM_PROMPT 

    def __call__(self, state: AgentState) -> dict: 
        """
        Основной метод узла, который принимает текущее состояние (state) 
        и возвращает обновленные данные.
        """
        
        # 1. Извлекаем текущий текстовый ввод пользователя из состояния
        user_input = state.get("input")
        
        # 2. Формируем "пакет" сообщений для отправки в модель.
        # Мы комбинируем три части:
        messages = [
            # А) Системная инструкция (всегда первая)
            SystemMessage(content=self.system_prompt),
            
            # Б) Вся накопленная история из AgentState.
            # Используем оператор *, чтобы "распаковать" список объектов BaseMessage
            *state.get("messages", []), 
            
            # В) Новое сообщение пользователя
            HumanMessage(content=user_input) 
        ]
        
        # 3. Передаем список объектов в модель.
        # Благодаря нашему конвертеру в YandexGPT.ask(), нам не нужно 
        # вручную преобразовывать эти объекты в словари {"role": "...", "content": "..."}
        response_text = self.model.ask(messages) 
        
        # 4. Возвращаем словарь, который LangGraph использует для обновления AgentState:
        return {
            # Обновляем поле output для вывода на экран
            "output": response_text,
            
            # Добавляем новые сообщения в историю.
            # Благодаря Annotated[..., add_messages] в AgentState, эти два сообщения
            # будут приклеены в конец существующего списка, а не заменят его.
            "messages": [
                HumanMessage(content=user_input), 
                AIMessage(content=response_text)
            ]
        }