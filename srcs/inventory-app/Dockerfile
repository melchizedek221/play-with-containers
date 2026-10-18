FROM python:3.9-slim

WORKDIR /usr/src

COPY requirements.txt ./

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install flask sqlalchemy psycopg2-binary python-dotenv Flask-SQLAlchemy

RUN env

COPY . .

EXPOSE 8080

CMD ["python3", "server.py"]
