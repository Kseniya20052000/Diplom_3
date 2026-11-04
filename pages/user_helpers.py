import random
import string
import time

def generate_unique_email() -> str:
    """Генерирует уникальный email для тестового пользователя."""
    suffix = f"{int(time.time())}{''.join(random.choices(string.ascii_lowercase, k=6))}"
    return f"qa_{suffix}@yandex.ru"


def get_default_password() -> str:
    """Возвращает стандартный пароль для тестовых пользователей."""
    return "Qa123456!"


def get_default_name() -> str:
    """Возвращает стандартное имя для тестовых пользователей."""
    return "Тест"
