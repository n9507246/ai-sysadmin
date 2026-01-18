from abc import ABC

# -------------------------------
# Базовый абстрактный класс ИИ-агента
# -------------------------------
class BaseAgent(ABC):

    def define_agent_state(self):
        # возвращаем уже объявленный тип
        return AgentState