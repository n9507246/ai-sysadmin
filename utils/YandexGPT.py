import os
import openai
from dotenv import load_dotenv
# Импортируем базовые классы сообщений LangChain для проверки типов
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

# Загружаем переменные окружения (API-ключи и ID папки) из файла .env
load_dotenv()

class YandexGPT():
    """
    Класс-адаптер для взаимодействия с YandexGPT.
    Преобразует высокоуровневые объекты сообщений LangChain в формат, 
    совместимый с OpenAI API, который используется в Yandex Cloud.
    """

    def __init__(self):
        # Инициализация клиента OpenAI SDK, настроенного на эндпоинт Yandex Cloud
        self.client = openai.OpenAI(
            api_key=os.getenv("YANDEX_CLOUD_API_KEY"),
            base_url="https://llm.api.cloud.yandex.net/v1",
            default_headers={
                "x-folder-id": os.getenv("YANDEX_CLOUD_FOLDER")
            },
        )

        # Формируем URI модели: gpt://<folder_id>/yandexgpt/latest
        self.model_path = (
            f"gpt://{os.getenv('YANDEX_CLOUD_FOLDER')}/yandexgpt/latest"
        )

    def _convert_messages(self, messages: list) -> list[dict]:
        """
        Конвертирует список объектов сообщений в формат словарей (JSON-like).
        
        Зачем это нужно:
        1. Разделение ответственности: Ваши узлы графа работают с объектами (HumanMessage, AIMessage),
           что удобно для логики LangGraph, но API Yandex ожидает простые словари с ключами 'role' и 'content'.
        2. Автоматизация: Метод избавляет от необходимости вручную писать {"role": "user", ...} в каждом узле.
        3. Гибкость: Если вы добавите новые типы сообщений, логику их обработки нужно будет изменить только здесь.
        """
        formatted_messages = []
        
        for msg in messages:
            # Если сообщение уже является словарем (прокидываем как есть)
            if isinstance(msg, dict):
                formatted_messages.append(msg)
                continue
            
            # Сопоставление классов LangChain с ролями API Yandex
            if isinstance(msg, HumanMessage):
                role = "user"        # Сообщение от человека
            elif isinstance(msg, AIMessage):
                role = "assistant"   # Ответ языковой модели
            elif isinstance(msg, SystemMessage):
                role = "system"      # Инструкция (системный промпт)
            else:
                role = "user"        # Резервный вариант
                
            # Добавляем в итоговый список словарь, понятный API
            formatted_messages.append({
                "role": role, 
                "content": msg.content
            })
            
        return formatted_messages

    def ask(
        self,
        messages: list, 
        max_tokens: int = 2000,
        temp: float = 0.3
    ) -> str:
        """
        Основной метод для генерации ответа.
        Принимает список сообщений (объекты или словари), выполняет конвертацию 
        и отправляет запрос в облако.
        """

        # 1. Приводим сообщения к единому формату словарей перед отправкой
        api_messages = self._convert_messages(messages)

        # 2. Выполняем HTTP-запрос через библиотеку openai
        response = self.client.chat.completions.create(
            model=self.model_path,
            messages=api_messages,
            max_tokens=max_tokens,
            temperature=temp,
        )

        # 3. Извлекаем только текст ответа
        return response.choices[0].message.content