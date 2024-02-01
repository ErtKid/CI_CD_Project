FROM python:3.8-slim



COPY backend/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

#Copy le backend et le frontend
COPY . /app


EXPOSE 5000

WORKDIR /app/backend

CMD ["flask", "run", "--host=0.0.0.0"]
