from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    ''' Состояние агента, содержащее входящий запрос и ответ модели. 
        input: str - Входящий запрос от пользователя
        output: str - Ответ, сформированный моделью
    '''
    input: str   # Входящий запрос от пользователя
    output: str  # Ответ, сформированный моделью
    messages: Annotated[list[BaseMessage], add_messages]
    summary: str  # Поле для хранения сжатого контекста