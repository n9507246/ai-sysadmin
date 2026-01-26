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

        :param model: LLM-модель, используемая для генерации summary
        :param instruction: Системная инструкция для суммаризации истории
        :param summary_threshold: Минимальное количество сообщений, при котором запускается суммаризация
        :param keep_last_messages_count: Количество последних сообщений, которые нужно сохранить 
    """
    
    model: Any
    instruction: str
    summary_threshold: int = 16
    keep_last_messages_count: int = 6
    
    def __call__(self, state: AgentState):
        
        # Создаём объект Messages для работы с историей сообщений, из состояния агента.
        messages = Messages( state )                                            


        # Выводим в консоль текущего состояния памяти.
        CliOutput.print_memory_state(messages.count,self.summary_threshold)                                           
                                                                     
                                                              
        # Если сообщений меньше порога суммаризации, то она не нужна
        if self._is_below_threshold(messages):
            # перерываем работу узла возвращая пустой объект                                  
            return {}                                                               

        # иначе(количество сообщений достигло порога сумморизации)             
        else:

            # вывродим сообщение что начинаем процесс сумморизации
            CliOutput.print_summary_start( self.summary_threshold )                  

            try:    
                
                # Делаем запрос к модели для генерации саммари 
                summary = self.model.ask([
                    { "role": "system", "content": self.instruction },                              # системное сообщение, в котором иструкцию для суммаризации 
                    { "role": "user", "content": f"Суммаризируй это:\n1{messages.to_text()}" },     # контент для суммморизации
                ]) 


                # Получаем список сообщений, которые должны быть удалены,
                messages_to_remove = messages.to_delete(
                    # передаем количество последних сообщений которые нужно сохранить 
                    # для того что бы LLM совсем не потерял контекст
                    self.keep_last_messages_count   
                )

                # Преобразуем сообщения в команды удаления (RemoveMessage),
                # которые понимает LangGraph / LangChain
                delete_messages: list[RemoveMessage] = []

                for message in messages_to_remove:
                    
                    # Некоторые сообщения могут не иметь id
                    # (например, системные или временные сообщения),
                    # такие сообщения нельзя удалить явно
                    if not message.id:
                        continue

                    # Создаём объект RemoveMessage по id сообщения
                    delete_messages.append(
                        RemoveMessage(id=message.id)
                    )


                # Отображает результат суммаризации: текст нового резюме, количество удалённых и оставленных сообщений
                CliOutput.print_summary_result(summary, len(delete_messages), self.keep_last_messages_count)

                # возвращаем сумморизацию и сообщение
                return {
                    "summary": summary,
                    "messages": delete_messages,
                }

            # Обрабатываем ошибки
            except Exception as e:
                # Выводим ошибку в консоль
                CliOutput.print_summary_error(e)
                # перерываем работу узла возвращая пустой объект  
                return {}

    def _is_below_threshold(self, messages: Messages) -> bool:
        """
        Проверяет, меньше ли количество сообщений в памяти порога суммаризации.

        :param messages: Объект Messages, содержащий текущую историю сообщений
        :return: True, если сообщений меньше порога, иначе False

        Этот метод используется для определения, нужно ли запускать процесс суммаризации.
        Если количество сообщений меньше `summary_threshold`, суммаризация не выполняется.
        """
        return messages.count < self.summary_threshold
