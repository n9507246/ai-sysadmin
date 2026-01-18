from core.BaseAgent import BaseAgent
from langgraph.graph import StateGraph, START, END
from agent.my_agent.AgentState import AgentState
from node.LLM import LLM

class Agent(BaseAgent): 
    """ Класс агента, внутри которого строится граф состояний. """
    
    def __init__(self):

        graph_builder = StateGraph(AgentState) # Инициализируем билдер графа с типом состояния AgentState
        graph_builder.add_node("ask_yandex_node", LLM()) # Добавляем узел для взаимодействия с LLM-моделью
        graph_builder.add_edge(START, "ask_yandex_node") # Соединяем старт с узлом LLM
        graph_builder.add_edge("ask_yandex_node", END) # Соединяем узел LLM с концом графа
        self.graph = graph_builder.compile() # Компилируем граф в исполняемый вид

    def run(self, user_message: str = '') -> AgentState:
        ''' Запускает агента с заданным пользовательским сообщением. '''
        return self.graph.invoke({
            "input": user_message, 
            "output": "",
        })