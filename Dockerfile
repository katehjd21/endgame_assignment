FROM python:3.13-slim

WORKDIR /app

COPY backend/ ./backend/
COPY frontend/ ./frontend/

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python3", "backend/app.py"]
