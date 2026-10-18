import json
from .models import get_db, create_order

def process_message(ch, method, properties, body):
    try:
        data = json.loads(body)
        user_id = data['user_id']
        number_of_items = data['number_of_items']
        total_amount = data['total_amount']

        db = next(get_db())
        create_order(db, user_id, number_of_items, total_amount)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Processed order for user {user_id}")
    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)