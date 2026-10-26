FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend ./backend
COPY frontend ./frontend
COPY data ./data
COPY openapi.yaml ./openapi.yaml

EXPOSE 8000

# SQLite DB lives in /app/data (mounted as a volume in docker-compose).
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
