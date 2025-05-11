FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install requests

# 🔧 добавляем утилиту sqlite3
RUN apt-get update && apt-get install -y sqlite3

CMD ["python", "main.py"]
