# Базовый лёгкий образ Python
FROM python:3.10-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем только зависимости (кэш Docker не будет пересобирать pip при изменении кода)
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Команда по умолчанию
CMD ["python3", "analysis.py"]
