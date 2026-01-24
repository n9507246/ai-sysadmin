import uuid
from rich.console import Console
from rich.panel import Panel
from langchain_core.messages import HumanMessage
from utils.FileReader import FileReader

# Инициализируем консоль
console = Console()

class FileReaderNode:
    def __init__(self):
        self.reader = FileReader()

    def __call__(self, state: dict) -> dict:
        output = state.get("output", "")
        
        try:
            # Извлекаем путь к файлу
            raw_path = output.split("READ_FILE:")[1].strip().split("\n")[0]
            clean_path = raw_path.strip("'\"`.,")
            
            if " " in clean_path:
                clean_path = clean_path.split(" ")[0].strip("'\"`.,")
            
            path = clean_path

            # ЛОГ: Короткое уведомление о действии
            console.print(f"[bold yellow]📂 Чтение файла:[/bold yellow] [cyan]{path}[/cyan]", end=" ")

            content = self.reader.read(path)
            
            # ЛОГ: Просто подтверждение успеха в той же строке
            console.print("[bold green]— ОК[/bold green]")

            result = f"Содержимое файла {path}:\n{content}"

        except Exception as e:
            # ЛОГ: Ошибка выделяется заметнее
            console.print("[bold red]— ОШИБКА[/bold red]")
            console.print(Panel(
                f"[bold red]Текст ошибки:[/bold red] {str(e)}\n[dim]Контекст: {output}[/dim]",
                title="❌ Ошибка FileReaderNode",
                border_style="red"
            ))
            result = f"Не удалось прочитать файл. Ответ модели был: {output}. Ошибка: {e}"

        return {
            "messages": [HumanMessage(content=result, id=str(uuid.uuid4()))]
        }