from dataclasses import dataclass
from agent.my_agent.AgentState import AgentState
from langchain_core.messages import RemoveMessage
from node.Summarizer.CliOutput import CliOutput
from typing import Any


@dataclass
class Summarizer:
    
    model: Any
    instruction: str
    summary_threshold: int = 16
    keep_messages: int = 6

    def __call__(self, state: AgentState):
        messages = state.get("messages", [])
        msg_count = len(messages)

        CliOutput.print_memory_state(msg_count, self.summary_threshold)

        if msg_count < self.summary_threshold:
            return {}

        CliOutput.print_summary_start(self.summary_threshold)

        history_text = "\n".join([f"{m.type}: {m.content}" for m in messages])
        prompt = [
            {"role": "system", "content": self.instruction},
            {"role": "user", "content": f"Суммаризируй это:\n{history_text}"},
        ]

        try:
            summary = self.model.ask(prompt)

            to_delete = messages[:-self.keep_messages]
            delete_messages = [RemoveMessage(id=m.id) for m in to_delete if m.id]

            CliOutput.print_summary_result(summary, len(delete_messages), self.keep_messages)

            return {
                "summary": summary,
                "messages": delete_messages,
            }

        except Exception as e:
            CliOutput.print_summary_error(e)
            return {}
