import json
from typing import Dict

import paho.mqtt.client as mqtt

import pika

CLOUD_CONFIG_FILE = '../configs/cloud_config.json'
PAHO_CLIENT_PUBLISH = 'v1/devices/me/telemetry'


def read_config_file() -> Dict:
    """Чтение данных из JSON файла."""
    try:
        with open(CLOUD_CONFIG_FILE, 'r') as file:
            cloud_settings = json.load(file)
    except FileExistsError:
        raise
    return cloud_settings


def get_paho_client(cloud_settings: Dict):
    """Создание клиента для подключения к облаку."""
    try:
        paho_client = mqtt.Client()
        paho_client.username_pw_set(cloud_settings.get('device_token'))
        paho_client.reconnect_delay_set(min_delay=1, max_delay=10)
        paho_client.connect(cloud_settings.get('cloud_url'),
                            cloud_settings.get('cloud_port'), 60)
        return paho_client
    except RuntimeError:
        raise


def callback(ch, method, properties, body):
    """Ожидание данных в очереди. Передача данных из очереди в облако."""
    data = body.decode('utf-8')
    paho_client.publish(PAHO_CLIENT_PUBLISH, data)
    paho_client.loop()


if __name__ == '__main__':
    cloud_settings = {}
    try:
        cloud_settings = read_config_file()
    except FileExistsError as err:
        print(f"Can't Read cloud_config File - {err}")

    try:
        paho_client = get_paho_client(cloud_settings=cloud_settings)
    except RuntimeError as err:
        print(f'Paho Error - {err}')

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    queue_to_main = connection.channel()
    queue_to_main.queue_declare(queue='mb-queue-put')
    queue_to_main.basic_consume('mb-queue-put', callback, auto_ack=True)
    try:
        queue_to_main.start_consuming()
    except KeyboardInterrupt:
        queue_to_main.stop_consuming()
    finally:
        connection.close()
