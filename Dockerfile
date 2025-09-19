# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем зависимости системы (нужны для psycopg2, Pillow и т.д.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .


# Открываем порт
EXPOSE 8000

# Запускаем gunicorn
CMD ["./entrypoint.sh"]