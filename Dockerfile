FROM python:3.8-slim

WORKDIR /app

COPY backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY backend /app
COPY frontend /app

CMD ["flask", "run", "--host=0.0.0.0"]
