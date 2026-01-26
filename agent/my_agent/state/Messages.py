from agent.my_agent.state.AgentState import AgentState
from langchain_core.messages import BaseMessage
from typing import List

class Messages:
    """
    Класс-обёртка для работы с сообщениями агента.
    """

    def __init__(self, state: AgentState):
        self._messages: List[BaseMessage] = state.get("messages", [])

    @property
    def count(self) -> int:


        return len(self._messages)

    def to_text(self) -> str:
        return "\n".join(
            f"{m.type}: {m.content}"
            for m in self._messages
            if hasattr(m, "content") and isinstance(m.content, str)
        )

    def to_delete(self, keep_last: int) -> List[BaseMessage]:
        if keep_last >= self.count:
            return []
        return self._messages[:-keep_last]

    # Для итерации в цикле: for m in messages
    def __iter__(self):
        return iter(self._messages)

    # Для срезов: messages[:-n]
    def __getitem__(self, index):
        return self._messages[index]
