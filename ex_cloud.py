import pika
import json

connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
queue_to_main = connection.channel()
queue_to_main.queue_declare(queue='mb-queue-put')
test_data = ({'slave_name': 'temperature', 'value': 30}, {'slave_name': 'humidity', 'value': 30})
jdata = json.dumps(test_data)
queue_to_main.basic_publish(
            exchange='',
            routing_key='mb-queue-put',
            body=jdata.encode('utf-8')
        )
connection.close()
