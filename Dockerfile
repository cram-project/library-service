FROM python:3.11-slim

WORKDIR /service

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY alembic.ini .
COPY src ./src

ENV PYTHONPATH=/service

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.library_service.main:app --host 0.0.0.0 --port 8000"]