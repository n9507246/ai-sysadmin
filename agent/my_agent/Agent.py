from core.BaseAgent import BaseAgent
from langgraph.graph import StateGraph, START, END
from agent.my_agent.AgentState import AgentState
from node.LLM import LLM
from node.Summarizer import Summarizer
from utils.YandexGPT import YandexGPT
from config import SYSTEM_PROMPT, SUMMARIZE_INSTRUCTION, SUMMARY_THRESHOLD

class Agent(BaseAgent): 
    def __init__(self, summary_threshold=16, keep_messages=6):
        llm_model = YandexGPT()
        graph_builder = StateGraph(AgentState)
        
        graph_builder.add_node("ask_yandex_node", LLM(model=llm_model, system_prompt=SYSTEM_PROMPT))
        
        # Настраиваем суммаризатор здесь
        graph_builder.add_node("summarize_node", Summarizer(
            model=llm_model, 
            instruction=SUMMARIZE_INSTRUCTION,
            summary_threshold=summary_threshold,
            keep_messages=keep_messages
        ))
        
        graph_builder.add_edge(START, "ask_yandex_node")
        graph_builder.add_edge("ask_yandex_node", "summarize_node")
        graph_builder.add_edge("summarize_node", END)
        
        self.graph = graph_builder.compile()

    def run(self, user_message: str, history: list = None, summary: str = "") -> dict:
        print(f"[LOG] Запуск итерации графа для сообщения: '{user_message[:20]}...'")
        return self.graph.invoke({
            "input": user_message, 
            "messages": history or [],
            "output": "",
            "summary": summary
        })
    