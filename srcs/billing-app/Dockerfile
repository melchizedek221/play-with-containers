FROM python:3.9-slim-bullseye

WORKDIR /usr/src

# COPY requirements.txt ./

# RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip3 install flask sqlalchemy pika python-dotenv Flask-SQLAlchemy psycopg2

COPY . .

EXPOSE 8080

CMD ["python", "server.py"]
