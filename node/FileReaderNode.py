import uuid
from langchain_core.messages import HumanMessage
from utils.FileReader import FileReader

class FileReaderNode:
    def __init__(self):
        self.reader = FileReader()
    def __call__(self, state: dict) -> dict:
        output = state.get("output", "")
        # Ожидаем команду вида: READ_FILE: /path/to/file
        try:
            # Извлекаем путь к файлу
            raw_path = output.split("READ_FILE:")[1].strip().split("\n")[0]
            print(f"[LOG] Извлеченный путь (сырой): '{raw_path}'")
            # Убираем лишние символы (кавычки, точки), если модель их добавила
            # Также обрабатываем случай, когда модель пишет комментарий после пути
            clean_path = raw_path.strip("'\"`.,")
            if " " in clean_path:
                clean_path = clean_path.split(" ")[0].strip("'\"`.,")
            path = clean_path
            print(f"[LOG] Очищенный путь: '{path}'")
            content = self.reader.read(path)
            result = f"Содержимое файла {path}:\n{content}"
        except Exception as e:
            print(f"[ERROR] Ошибка в FileReaderNode: {e}")
            result = f"Не удалось прочитать файл. Ответ модели был: {output}. Ошибка: {e}"

        # Возвращаем результат как HumanMessage, чтобы модель увидела его в истории
        return {
            "messages": [HumanMessage(content=result, id=str(uuid.uuid4()))]
        }