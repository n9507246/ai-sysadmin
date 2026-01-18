import os
import openai
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()


class YandexGPT():
    """
    Класс для работы с языковой моделью YandexGPT через API Yandex Cloud.
    Позволяет отправлять сообщения модели и получать текстовые ответы.
    """

    def __init__(self):
        # Создаём клиента для работы с API YandexGPT
        # Используем ключ и ID папки из переменных окружения
        self.client = openai.OpenAI(
            api_key=os.getenv("YANDEX_CLOUD_API_KEY"),  # API-ключ для доступа
            base_url="https://llm.api.cloud.yandex.net/v1",  # адрес API
            default_headers={
                "x-folder-id": os.getenv("YANDEX_CLOUD_FOLDER")  # идентификатор папки в облаке
            },
        )

        # Путь к модели YandexGPT в формате Yandex Cloud
        self.model_path = (
            f"gpt://{os.getenv('YANDEX_CLOUD_FOLDER')}/yandexgpt/latest"
        )

    def ask(
        self,
        messages: list[dict],  # список сообщений в формате {"role": "user/assistant/system", "content": "..."}
        max_tokens: int = 2000,  # максимальное количество токенов в ответе
        temp: float = 0.3        # температура генерации (чем меньше, тем точнее ответы)
    ) -> str:
        """
        Отправляет сообщения модели YandexGPT и возвращает её текстовый ответ.

        Параметры:
            messages (list[dict]): переписка с моделью.
            max_tokens (int): лимит токенов в ответе.
            temp (float): креативность ответа (температура).

        Возвращает:
            str: текстовый ответ модели.
        """

        # Отправляем запрос в модель через API
        response = self.client.chat.completions.create(
            model=self.model_path,  # модель, с которой работаем
            messages=messages,      # переписка
            max_tokens=max_tokens,  # ограничение длины ответа
            temperature=temp,       # креативность
        )

        # Возвращаем текст ответа модели
        return response.choices[0].message.content
