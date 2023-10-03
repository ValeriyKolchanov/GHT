import pika
from time import sleep
from random import randint


# def callback(ch, method, properties, body):
#     result = body.decode('utf-8')
#     print(result, type(result))


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
queue_from_main = connection.channel()
queue_from_main.queue_declare(queue='logic-queue')
arr = ['name_1', 'name_2', 'name_3']
body = ' '.join(arr)
queue_from_main.basic_publish(exchange='', routing_key='logic-queue', body=body.encode('utf-8'))

# queue_from_main.basic_consume('mb-queue-get', callback, auto_ack=True)
#
# try:
#     queue_from_main.start_consuming()
# except KeyboardInterrupt:
#     queue_from_main.stop_consuming()
# finally:
#     connection.close()
# body = [
#     "{'slave_name': 'Relay-10', 'value': '256'}",
#     "{'slave_name': 'Relay-11', 'value': '512'}",
#     "{'slave_name': 'Relay-12', 'value': '768'}",
#     "{'slave_name': 'Relay-13', 'value': '768'}",
#     "{'slave_name': 'Relay-14', 'value': '768'}",
#     "{'slave_name': 'Relay-15', 'value': '768'}",
# ]
# try:
#     while True:
#         body = input()
#         queue_from_main.basic_publish(
#             exchange='',
#             routing_key='mb-queue-get',
#             body=body.encode('utf-8')
#         )
# except KeyboardInterrupt:
#     connection.close()
#     raise
