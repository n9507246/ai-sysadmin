import subprocess
import uuid
from rich.panel import Panel
from langchain_core.messages import HumanMessage
from utils.logger import console

class CommandExecutorNode:
    def __call__(self, state: dict) -> dict:
        output = state.get("output", "")
        
        try:
            # Парсим команду. Ожидаем формат: EXECUTE: <команда>
            if "EXECUTE:" not in output:
                return {"messages": [HumanMessage(content="Ошибка: Команда не найдена в ответе агента.", id=str(uuid.uuid4()))]}

            command = output.split("EXECUTE:")[1].strip().split("\n")[0].strip()

            # Очистка команды от артефактов разметки
            command = command.rstrip(" ).,")
            command = command.replace("**", "").replace("`", "").strip()

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
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=120  # Увеличил до 2 минут для тяжелых установок
            )
            
            if result.returncode == 0:
                console.print(f"[bold green]— OK[/bold green]")
                
                # Показываем полный вывод в терминале для тебя
                if result.stdout and result.stdout.strip():
                    console.print(Panel(result.stdout.strip(), title="[bold green]STDOUT[/bold green]", border_style="green"))

                # --- УМНАЯ ФИЛЬТРАЦИЯ ДЛЯ ИСТОРИИ (Экономим токены) ---
                lines = result.stdout.splitlines()
                
                # 1. Скрываем подробности пакетных менеджеров при успехе
                noisy_commands = ['apt', 'install', 'update', 'upgrade', 'dpkg', 'mysql-server']
                if any(c in command for c in noisy_commands):
                    stdout_for_ai = "[Команда выполнена успешно. Подробный лог скрыт для экономии контекста.]"
                
                # 2. Если вывод длинный (например, список файлов или статус), делаем "сэндвич"
                elif len(lines) > 30:
                    stdout_for_ai = "\n".join(
                        lines[:15] + 
                        [f"\n... [обрезано {len(lines)-30} строк для экономии токенов] ...\n"] + 
                        lines[-15:]
                    )
                else:
                    stdout_for_ai = result.stdout.strip()
                
                response_text = f"--- STDOUT (Код 0) ---\n{stdout_for_ai}"
            
            else:
                console.print(f"[bold red]— FAIL[/bold red]")
                
                # Если ошибка — показываем всё в терминале
                error_view = f"[bold red]STDERR:[/bold red]\n{result.stderr}\n\n[dim]STDOUT:[/dim]\n{result.stdout}"
                console.print(Panel(error_view, title=f"[bold red]EXIT CODE {result.returncode}[/bold red]", border_style="red"))

                # Для ИИ при ошибке тоже чуть-чуть подрезаем, чтобы не «вылететь» за лимиты
                # Но оставляем достаточно данных для диагностики
                response_text = (
                    f"--- STDERR (Код {result.returncode}) ---\n{result.stderr[:1500]}\n"
                    f"--- STDOUT ---\n{result.stdout[:1000]}"
                )

            final_msg = f"РЕЗУЛЬТАТ КОМАНДЫ '{command}':\n{response_text}"

        except Exception as e:
            console.print(f"[bold red]— ОШИБКА ЗАПУСКА: {e}[/bold red]")
            final_msg = f"СИСТЕМНАЯ ОШИБКА при попытке запуска команды: {e}"

        return {
            "messages": [HumanMessage(content=final_msg, id=str(uuid.uuid4()))]
        }