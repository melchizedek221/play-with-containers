from flask import Flask, request, jsonify
from importlib.metadata import version
from flask_restx import Api, Resource, fields
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pika
import json
import requests
import os
import time

load_dotenv()

# Assume we have a simple database to store failed messages
# In a real-world scenario, you'd use a proper database like PostgreSQL or MongoDB
failed_messages = []

app = Flask(__name__)
api = Api(app, version='1.0', title='Gateway API',
    description='A gateway API for movie inventory and billing')

# Namespaces
movies_ns = api.namespace('api/movies', description='Movie operations')
billing_ns = api.namespace('api/billing', description='Billing operations')

# Configuration RabbitMQ
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')

INVENTORY_API_URL= os.getenv('INVENTORY_API_URL')

# Models
movie_model = api.model('Movie', {
    'id': fields.Integer(readonly=True, description='The movie identifier'),
    'title': fields.String(required=True, description='The movie title'),
    'description': fields.String(required=True, description='The description of the movie'),
})

billing_model = api.model('BillingRequest', {
    # Define the structure of your billing request
    'user_id': fields.String(required=True, description='The user identifier'),
    'movie_id': fields.Integer(required=True, description='The movie identifier'),
    'amount': fields.Float(required=True, description='The billing amount')
})
@movies_ns.route('/')
class MovieList(Resource):
    @movies_ns.doc('list_movies')
    @movies_ns.response(200, 'Success')
    def get(self):
        """List all movies"""
        return proxy_inventory()

    @movies_ns.doc('create_movie')
    @movies_ns.expect(movie_model)
    @movies_ns.response(201, 'Movie created')
    def post(self):
        """Create a new movie"""
        return proxy_inventory()

@movies_ns.route('/<int:id>')
@movies_ns.response(404, 'Movie not found')
@movies_ns.param('id', 'The movie identifier')
class Movie(Resource):
    @movies_ns.doc('get_movie')
    @movies_ns.response(200, 'Success')
    def get(self, id):
        """Fetch a movie given its identifier"""
        return proxy_inventory(id)

    @movies_ns.doc('update_movie')
    @movies_ns.expect(movie_model)
    @movies_ns.response(200, 'Movie updated')
    def put(self, id):
        """Update a movie given its identifier"""
        return proxy_inventory(id)

    @movies_ns.doc('delete_movie')
    @movies_ns.response(204, 'Movie deleted')
    def delete(self, id):
        """Delete a movie given its identifier"""
        return proxy_inventory(id)    

@app.route('/api/movies/', methods=['GET', 'POST', 'DELETE'])
@app.route('/api/movies/<int:id>', methods=['GET', 'PUT', 'DELETE'])

def proxy_inventory(id=None):
    if id:
        url = f'{INVENTORY_API_URL}/api/movies/{id}'
    else:
        url = f'{INVENTORY_API_URL}/api/movies/'    
    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = app.response_class(
        response=resp.content,
        status=resp.status_code,
        headers=headers,
    )
    return response

def publish_to_rabbitmq(message):
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=credentials
        ))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # rendre le message persistant
            )
        )
        connection.close()
        print("Message sent to RabbitMQ")
        return True
    except Exception as e:
        print(f"Error while sending message to RabbitMQ: {e}")
        return False

@app.route('/api/billing', methods=['POST'])
def billing():
    try:
        # Récupérer le corps de la requête POST en JSON
        message = request.json
        
        # Publier le message dans RabbitMQ
        success= publish_to_rabbitmq(message)
        if success:
        # Répondre avec une confirmation
            return jsonify({"message": "Message posted successfully"}), 200
        else:
             # Store failed message for retry
            failed_messages.append({
                'message': message,
                'attempts': 0,
                'next_attempt': datetime.now()
            })
            return jsonify({"message": "Request accepted but not processed. It will be retried later."}), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@billing_ns.route('/')
class Billing(Resource):
    @billing_ns.doc('create_billing')
    @billing_ns.expect(billing_model)
    @billing_ns.response(200, 'Message posted successfully')
    @billing_ns.response(500, 'Internal server error')
    def post(self):
        """Create a new billing request"""
        try:
            message = request.json
            publish_to_rabbitmq(message)
            return {"message": "Message posted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500


def retry_failed_messages():
    current_time = datetime.now()
    
    for failed_message in failed_messages[:]:  # Create a copy of the list to iterate over
        if current_time >= failed_message['next_attempt']:
            success = publish_to_rabbitmq(failed_message['message'])
            
            if success:
                failed_messages.remove(failed_message)
                print(f"Successfully retried message: {failed_message['message']}")
            else:
                failed_message['attempts'] += 1
                
                # Implement exponential backoff
                delay = min(300, 2 ** failed_message['attempts'])  # Cap at 5 minutes
                failed_message['next_attempt'] = current_time + timedelta(seconds=delay)
                
                print(f"Retry failed for message: {failed_message['message']}. "
                      f"Next attempt in {delay} seconds.")
                
                # If we've tried too many times, we might want to move this to a dead-letter queue
                if failed_message['attempts'] >= 1000:
                    print(f"Message failed too many times, moving to dead-letter queue: {failed_message['message']}")
                    # Implement dead-letter queue logic here
                    failed_messages.remove(failed_message)

# This function should be called periodically, e.g., by a cron job or a background task
def run_retry_process():
    while True:
        retry_failed_messages()
        time.sleep(5)  # Wait for 5 second before the next retry attempt

if __name__ == '__main__':
    # Start the retry process in a separate thread
    import threading
    retry_thread = threading.Thread(target=run_retry_process, daemon=True)
    retry_thread.start()
    app.run(host='0.0.0.0', port=3000)
