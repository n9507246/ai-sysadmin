import os
import subprocess

class FileReader:
    def read(self, file_path: str) -> str:
        """Читает содержимое файла по указанному пути."""
        if os.path.isdir(file_path):
            try:
                files = os.listdir(file_path)
                return f"Это директория {file_path}. Содержимое: {', '.join(files)}"
            except Exception as e:
                return f"Ошибка при чтении директории {file_path}: {e}"

        if not os.path.exists(file_path):
            msg = f"Ошибка: Файл {file_path} не найден."
            directory = os.path.dirname(file_path) or "."
            if os.path.isdir(directory):
                try:
                    files = os.listdir(directory)
                    msg += f" Содержимое директории {directory}: {', '.join(files)}"
                except Exception:
                    pass
            return msg
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as original_e:
            # Если обычное чтение не удалось (например, Permission denied), пробуем через sudo
            try:
                # sudo -n предотвращает зависание на вводе пароля
                cmd = ["sudo", "-n", "cat", file_path]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    content = result.stdout
                else:
                    return f"Ошибка при чтении файла {file_path}: {original_e}. Sudo ошибка: {result.stderr.strip()}"
            except Exception:
                return f"Ошибка при чтении файла {file_path}: {original_e}"

        # Обрезаем контент, если он слишком большой (лимит ~20000 символов)
        MAX_CHARS = 20000
        if len(content) > MAX_CHARS:
            half = MAX_CHARS // 2
            content = content[:half] + f"\n\n... [Слишком длинный файл. Обрезано {len(content) - MAX_CHARS} символов] ...\n\n" + content[-half:]
            
        return content