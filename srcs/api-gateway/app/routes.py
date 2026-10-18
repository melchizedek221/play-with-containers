from flask import request, jsonify
from app import app, channel
import requests
import json
import os

INVENTORY_API_URL= f'{os.getenv('INVENTORY_API_URL')}'
@app.route('/api/movies/', methods=['GET', 'POST', 'DELETE'])
@app.route('/api/movies/<int:id>', methods=['GET', 'PUT', 'DELETE'])

def proxy_inventory(id=None):
    if id:
        url = f"{INVENTORY_API_URL}/api/movies/{id}"
    else:
        url = f"{INVENTORY_API_URL}/api/movies/"
    
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

@app.route('/api/billing', methods=['POST'])
def billing():
    message = json.dumps(request.json)
    channel.basic_publish(exchange='',
                          routing_key='billing_queue',
                          body=message)
    return jsonify({"message": "Billing request posted"}), 202