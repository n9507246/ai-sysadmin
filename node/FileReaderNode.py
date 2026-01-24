import uuid
from rich.panel import Panel
from langchain_core.messages import HumanMessage
from utils.FileReader import FileReader
from utils.logger import console

class FileReaderNode:
    def __init__(self):
        self.reader = FileReader()

    def __call__(self, state: dict) -> dict:
        output = state.get("output", "")
        
        try:
            # Парсинг пути
            raw_path = output.split("READ_FILE:")[1].strip().split("\n")[0]
            path = raw_path.strip("'\"`.,").split(" ")[0].strip("'\"`.,")

            # Логируем в твой Tilix
            console.print(f"    [bold yellow]📂 Чтение файла:[/bold yellow] [cyan]{path}[/cyan]", end=" ")

            content = self.reader.read(path)
            
            console.print(f"    Чтение файла {path}. [bold green]— ОК[/bold green]")

            # Формируем ответ для модели (чтобы она знала, ЧТО прочитала)
            # Добавляем явное указание пути в начало контента
            result = f"--- СИСТЕМНОЕ УВЕДОМЛЕНИЕ ---\nУспешно прочитан файл: {path}\n\nСодержимое:\n{content}"

        except Exception as e:
            console.print("[bold red]— ОШИБКА[/bold red]")
            console.print(Panel(
                f"[bold red]Текст ошибки:[/bold red] {str(e)}\n[dim]Контекст: {output}[/dim]",
                title="❌ Ошибка FileReaderNode",
                border_style="red"
            ))
            result = f"ОШИБКА: Не удалось прочитать файл по пути {path if 'path' in locals() else 'неизвестно'}. Ошибка: {e}"

        return {
            # Возвращаем это в историю сообщений
            "messages": [HumanMessage(content=result, id=str(uuid.uuid4()))]
        }