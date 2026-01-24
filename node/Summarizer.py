import uuid
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from agent.my_agent.AgentState import AgentState
from langchain_core.messages import RemoveMessage
from utils.logger import console

class Summarizer:
    def __init__(self, model, instruction, summary_threshold: int = 16, keep_messages: int = 6):
        self.model = model
        self.instruction = instruction
        self.summary_threshold = summary_threshold
        self.keep_messages = keep_messages

    def __call__(self, state: AgentState):
        messages = state.get("messages", [])
        msg_count = len(messages)

        # Лаконичный лог текущего состояния
        console.print(f"\n[dim]─── Память: {msg_count}/{self.summary_threshold} сообщений ───[/dim]\n")

        if msg_count < self.summary_threshold:
            return {} 

        # Визуальный акцент на запуске суммаризации
        console.print(Panel(
            f"[bold yellow]Порог ({self.summary_threshold}) превышен![/bold yellow]\n"
            f"Запускаю процесс сжатия истории...",
            border_style="yellow"
        ))
        
        history_text = "\n".join([f"{m.type}: {m.content}" for m in messages])
        prompt = [
            {"role": "system", "content": self.instruction},
            {"role": "user", "content": f"Суммаризируй это:\n{history_text}"}
        ]
        
        try:
            summary = self.model.ask(prompt)
            
            # Сообщения для удаления
            to_delete = messages[:-self.keep_messages]
            delete_messages = [RemoveMessage(id=m.id) for m in to_delete if m.id]
            
            # Красивый отчет о результате
            summary_panel = Panel(
                f"[italic white]{summary}[/italic white]",
                title="[bold green]Новое резюме памяти (Summary)[/bold green]",
                border_style="green",
                padding=(1, 2)
            )
            
            stats_text = Text.assemble(
                ("Удалено: ", "bold red"), (f"{len(delete_messages)} ", "red"),
                ("Оставлено: ", "bold cyan"), (f"{self.keep_messages}", "cyan")
            )
            
            console.print(summary_panel)
            console.print(stats_text)
            console.print("[dim]──────────────────────────────────────────[/dim]\n")

            return {
                "summary": summary, 
                "messages": delete_messages 
            }
        except Exception as e:
            console.print(f"[bold red]❌ Ошибка суммаризации:[/bold red] {e}")
            return {}