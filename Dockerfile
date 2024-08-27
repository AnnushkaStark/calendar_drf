FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y supervisor

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main_app.wsgi"]