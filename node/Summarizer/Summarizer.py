from dataclasses import dataclass
from agent.my_agent.state.AgentState import AgentState
from langchain_core.messages import RemoveMessage
from node.Summarizer.CliOutput import CliOutput
from typing import Any
from agent.my_agent.state.Messages import Messages


@dataclass
class Summarizer:
    """
    Класс для суммаризации истории сообщений агента.
    """
    model: Any
    instruction: str
    summary_threshold: int = 16
    keep_messages: int = 6

    def __call__(self, state: AgentState):
        
        messages = Messages(state) # Создаём объект Messages для работы с историей
        CliOutput.print_memory_state(messages.count, self.summary_threshold) # Печать текущего состояния памяти

        # Проверка: достигнут ли порог для суммаризации
        if self._is_below_threshold(messages):
            # Если сообщений меньше порога — суммаризация не нужна
            return {}

        
        CliOutput.print_summary_start(self.summary_threshold)   # Порог превышен — запускаем суммаризацию

       
        history_text = messages.to_text()  # Генерируем текст всей истории через Messages
        prompt = [
            {"role": "system", "content": self.instruction},
            {"role": "user", "content": f"Суммаризируй это:\n{history_text}"},
        ]

        try:
            
            summary = self.model.ask(prompt) # Получаем резюме от модели

            # Сообщения, которые нужно удалить
            delete_messages = [
                RemoveMessage(id=m.id) for m in messages.to_delete(self.keep_messages) if m.id
            ]

            # Печать результата суммаризации
            CliOutput.print_summary_result(summary, len(delete_messages), self.keep_messages)

            return {
                "summary": summary,
                "messages": delete_messages,
            }

        except Exception as e:
            # Ошибка суммаризации
            CliOutput.print_summary_error(e)
            return {}

    # ───────────── Приватные методы ─────────────

    def _is_below_threshold(self, messages: Messages) -> bool:
        """
        Проверяет, меньше ли количество сообщений в памяти порога суммаризации.

        :param messages: Объект Messages, содержащий текущую историю сообщений
        :return: True, если сообщений меньше порога, иначе False

        Этот метод используется для определения, нужно ли запускать процесс суммаризации.
        Если количество сообщений меньше `summary_threshold`, суммаризация не выполняется.
        """
        return messages.count < self.summary_threshold
