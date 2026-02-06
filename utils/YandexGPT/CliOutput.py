from rich.panel import Panel
from utils.logger import console

class CliOutput:
    """Класс для всех визуальных и текстовых выводов Summarizer в консоль."""

    @staticmethod
    def print_token_usage(prompt_tokens: int, completion_tokens: int, total_tokens: int) -> None:
        """
        Выводит информацию об использовании токенов.
        
        :param prompt_tokens: Количество токенов в запросе
        :param completion_tokens: Количество токенов в ответе
        :param total_tokens: Общее количество токенов
        """
        console.print(f"[dim]─── Токены: запрос {prompt_tokens}, ответ {completion_tokens}, всего {total_tokens} ───[/dim]\n")