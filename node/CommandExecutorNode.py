import subprocess
import uuid
from rich.panel import Panel
from langchain_core.messages import HumanMessage
from utils.logger import console

class CommandExecutorNode:
    def __call__(self, state: dict) -> dict:
        output = state.get("output", "")
        
        try:

            print('output =====================>  ', output )


            # Парсим команду. Ожидаем формат: EXECUTE: <команда>
            # Берем первую строку после метки
            command = output.split("EXECUTE:")[1].strip().split("\n")[0].strip()
            
            # Парсим команду. Ожидаем формат: EXECUTE: <команда>
            # Берем первую строку после метки
            command = output.split("EXECUTE:")[1].strip().split("\n")[0].strip()

            # Убираем завершающие скобки, точки и лишние символы
            command = command.rstrip(" ).,")

            # Убираем Markdown-символы: жирный текст ** и обратные кавычки `
            command = command.replace("**", "").replace("`", "").strip()

            
            print('command =====================>  ', command )

            # Автоматически добавляем -y к командам apt/apt-get, чтобы избежать зависания
            # в ожидании подтверждения от пользователя [Y/n], которое приводит к таймауту.
            # if "apt" in command and "-y" not in command:
            #     # Используем f-строку с пробелами, чтобы заменять только целые слова "install" или "upgrade"
            #     if " install " in f" {command} ":
            #         command = f" {command} ".replace(" install ", " install -y ").strip()
            #     elif " upgrade " in f" {command} ":
            #         command = f" {command} ".replace(" upgrade ", " upgrade -y ").strip()
            
            # --- БЛОК ПОДТВЕРЖДЕНИЯ ---
            console.print(f"\n[bold yellow]⚡ Агент предлагает выполнить команду:[/bold yellow] [cyan]{command}[/cyan]")
            confirm = console.input("[bold yellow]   Выполнить? (y/n): [/bold yellow]")
            
            if confirm.lower() not in ["y", "yes"]:
                console.print("[bold red]   ⛔ Отменено пользователем.[/bold red]")
                return {
                    "messages": [HumanMessage(content=f"Пользователь ОТКЛОНИЛ выполнение команды: {command}", id=str(uuid.uuid4()))]
                }
            # --------------------------

            console.print(f"    [bold red]🚀 Выполнение:[/bold red] [cyan]{command}[/cyan]", end=" ")

            # Запускаем команду
            # shell=True позволяет использовать пайпы (|) и перенаправления (>), 
            # что важно для администрирования.
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=60 # Таймаут 60 секунд на всякий случай
            )
            
            if result.returncode == 0:
                console.print(f"[bold green]— OK[/bold green]")
                
                # Если есть вывод, показываем его пользователю в красивой рамке
                if result.stdout and result.stdout.strip():
                    console.print(Panel(result.stdout.strip(), title="[bold green]STDOUT[/bold green]", border_style="green"))

                # Ограничиваем вывод, чтобы не забить контекст (первые 4000 символов)
                stdout_trunc = result.stdout[:4000] 
                response = f"--- STDOUT (Код 0) ---\n{stdout_trunc}"
            else:
                console.print(f"[bold red]— FAIL[/bold red]")
                
                # Если ошибка, показываем STDERR и STDOUT
                error_view = f"[bold red]STDERR:[/bold red]\n{result.stderr}\n\n[dim]STDOUT:[/dim]\n{result.stdout}"
                console.print(Panel(error_view, title=f"[bold red]EXIT CODE {result.returncode}[/bold red]", border_style="red"))

                response = f"--- STDERR (Код {result.returncode}) ---\n{result.stderr}\n--- STDOUT ---\n{result.stdout}"

            final_msg = f"РЕЗУЛЬТАТ КОМАНДЫ '{command}':\n{response}"

        except Exception as e:
            console.print(f"[bold red]— ОШИБКА ЗАПУСКА: {e}[/bold red]")
            final_msg = f"СИСТЕМНАЯ ОШИБКА при попытке запуска команды: {e}"

        return {
            "messages": [HumanMessage(content=final_msg, id=str(uuid.uuid4()))]
        }