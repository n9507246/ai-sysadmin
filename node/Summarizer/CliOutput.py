from rich.panel import Panel
from rich.text import Text
from utils.logger import console

class CliOutput:
    """Класс для всех визуальных и текстовых выводов Summarizer в консоль."""

    @staticmethod
    def print_memory_state(current: int, threshold: int) -> None:
        console.print(f"\n[dim]─── Память: {current}/{threshold} сообщений ───[/dim]\n")

    @staticmethod
    def print_summary_start(threshold: int) -> None:
        console.print(
            Panel(
                f"[bold yellow]Порог ({threshold}) превышен![/bold yellow]\n"
                "Запускаю процесс сжатия истории...",
                border_style="yellow",
            )
        )

    @staticmethod
    def print_summary_result(summary: str, deleted: int, kept: int) -> None:
        console.print(
            Panel(
                f"[italic white]{summary}[/italic white]",
                title="[bold green]Новое резюме памяти (Summary)[/bold green]",
                border_style="green",
                padding=(1, 2),
            )
        )

        stats_text = Text.assemble(
            ("Удалено: ", "bold red"), (f"{deleted} ", "red"),
            ("Оставлено: ", "bold cyan"), (f"{kept}", "cyan"),
        )
        console.print(stats_text)
        console.print("[dim]──────────────────────────────────────────[/dim]\n")

    @staticmethod
    def print_summary_error(error: Exception) -> None:
        console.print(f"[bold red]❌ Ошибка суммаризации:[/bold red] {error}")
