from rich.panel import Panel
from rich.markdown import Markdown
from utils.logger import console  # Глобальный консоль
from agent.my_agent.Agent import Agent
from core.MemoryManager import MemoryManager
from config import HISTORY_MAX_ENTRIES, SUMMARY_THRESHOLD, KEEP_MESSAGES

def main():
    agent = Agent(summary_threshold=SUMMARY_THRESHOLD, keep_messages=KEEP_MESSAGES)
    memory = MemoryManager("history.json", max_entries=HISTORY_MAX_ENTRIES)
    
    console.print("\n")
    console.print(Panel.fit(
        f"[bold green]Запущено![/bold green]\n"
        f"Порог суммаризации: [yellow]{SUMMARY_THRESHOLD}[/yellow]\n"
        f"Храним сообщений: [yellow]{KEEP_MESSAGES}[/yellow]",
        title="Система управления знаниями"
    ))

    while True:
        try:
            user_input = console.input("\n[bold cyan]❱❱❱ Вы:[/bold cyan] ")
            
            if user_input.lower() in ("exit", "quit"):
                console.print("[bold red]Завершение работы...[/bold red]")
                break

            # Создаем статус
            with console.status("[bold blue]Агент думает...", spinner="dots") as status:
                # ВАЖНО: передаем объект status в агент, если хотим им управлять
                # Или просто полагаемся на то, что Nodes используют тот же console
                result = agent.run(
                    user_input, 
                    history=memory.get_history(),
                    summary=memory.get_summary()
                )

                updated_messages = result.get("messages", [])
                updated_summary = result.get("summary") or memory.get_summary()
                memory.add_messages(updated_messages, summary=updated_summary)

            # После выхода из 'with' спиннер удаляется автоматически. 
            # Теперь выводим ответ.
            ai_content = Markdown(result['output'])
            console.print(
                Panel(
                    ai_content,
                    title="[bold magenta]AI Assistant[/bold magenta]",
                    border_style="bright_blue",
                    padding=(1, 2)
                )
            )

        except KeyboardInterrupt:
            console.print("\n[bold red]Прервано пользователем[/bold red]")
            break

if __name__ == "__main__":
    main()