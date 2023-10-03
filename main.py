from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pika
from time import sleep

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    body = request.json['button_value']
    channel.basic_publish(exchange='', routing_key='mb-queue-get', body=body.encode('utf-8'))
    return jsonify({'result': 'Success!'})


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue='mb-queue-get')
    app.run(host='0.0.0.0', debug=True)
