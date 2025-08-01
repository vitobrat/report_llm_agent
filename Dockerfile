FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install --no-cache-dir poetry==1.8.2

# Создание и настройка рабочей директории
WORKDIR /app
ENV PYTHONPATH=/app

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock ./

# Установка зависимостей в системный Python
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Копирование остального кода
COPY . .

# Экспозиция порта
EXPOSE 8000

# Запуск сервера через модуль uvicorn (надежный способ)
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]