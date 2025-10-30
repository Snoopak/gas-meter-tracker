# Використовуємо офіційний Python образ
FROM python:3.11-slim

# Встановлюємо системні залежності включно з Tesseract OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-ukr \
    tesseract-ocr-eng \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файл залежностей
COPY requirements.txt .

# Встановлюємо Python залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі файли проекту
COPY . .

# Встановлюємо змінну середовища для Flask
ENV FLASK_APP=web_app.py

# Відкриваємо порт (Render автоматично призначить PORT)
EXPOSE 10000

# Команда запуску (Render передає PORT через змінну середовища)
CMD gunicorn web_app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1
