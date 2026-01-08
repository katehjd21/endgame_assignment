FROM python:3.13-slim

WORKDIR /app

COPY backend/ ./backend/
COPY frontend/ ./frontend/

COPY backend/requirements.txt ./backend/
COPY frontend/requirements.txt ./frontend/
RUN pip install --upgrade pip \
    && pip install -r backend/requirements.txt \
    && pip install -r frontend/requirements.txt

EXPOSE 8080

CMD ["python3", "backend/app.py"]