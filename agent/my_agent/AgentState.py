from typing import TypedDict

class AgentState(TypedDict):
    ''' Состояние агента, содержащее входящий запрос и ответ модели. 
        input: str - Входящий запрос от пользователя
        output: str - Ответ, сформированный моделью
    '''
    input: str   # Входящий запрос от пользователя
    output: str  # Ответ, сформированный моделью