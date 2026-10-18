from flask import Flask
import pika
import json
import os

app = Flask(__name__)

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST')))
channel = connection.channel()
channel.queue_declare(queue='billing_queue')

from app import routes