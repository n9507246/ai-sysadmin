import uuid
from langchain_core.messages import HumanMessage
from core.BaseAgent import BaseAgent
from langgraph.graph import StateGraph, START, END
from agent.my_agent.state.AgentState import AgentState
from node.LLM import LLM
from node.Summarizer.Summarizer import Summarizer
from node.FileReaderNode import FileReaderNode
from node.CommandExecutorNode import CommandExecutorNode
from utils.YandexGPT.YandexGPT import YandexGPT
from config import SYSTEM_PROMPT, SUMMARIZE_INSTRUCTION

class Agent(BaseAgent): 
    def __init__(self, summary_threshold=16, keep_messages=6):
        llm_model = YandexGPT()
        graph_builder = StateGraph(AgentState)

        graph_builder.add_node("ask_yandex_node", LLM(model=llm_model, system_prompt=SYSTEM_PROMPT))
        graph_builder.add_node("read_file_node", FileReaderNode())
        graph_builder.add_node("command_node", CommandExecutorNode())

        # Настраиваем суммаризатор здесь
        graph_builder.add_node("summarize_node", Summarizer(
            model=llm_model, 
            instruction=SUMMARIZE_INSTRUCTION,
            summary_threshold=summary_threshold,
            keep_last_messages_count=keep_messages
        ))
        
        # Логика маршрутизации
        def route_logic(state):
            if "READ_FILE:" in state["output"]:
                return "read_file"
            if "EXECUTE:" in state["output"]:
                return "execute_command"
            return "summarize"

        graph_builder.add_edge(START, "ask_yandex_node")
        
        graph_builder.add_conditional_edges(
            "ask_yandex_node",
            route_logic,
            {
                "read_file": "read_file_node",
                "execute_command": "command_node",
                "summarize": "summarize_node"
            }
        )
        
        graph_builder.add_edge("read_file_node", "ask_yandex_node")
        graph_builder.add_edge("command_node", "ask_yandex_node")
        graph_builder.add_edge("summarize_node", END)
        
        self.graph = graph_builder.compile()

    def run(self, user_message: str, history: list = None, summary: str = "") -> dict:
        # print(f"[LOG] Запуск итерации графа для сообщения: '{user_message[:20]}...'")
        
        # Добавляем сообщение пользователя в историю перед запуском графа
        history = history or []
        history.append(HumanMessage(content=user_message, id=str(uuid.uuid4())))
        
        return self.graph.invoke({
            "input": user_message, 
            "messages": history,
            "output": "",
            "summary": summary
        })
    