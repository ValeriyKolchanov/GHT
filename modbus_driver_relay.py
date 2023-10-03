import json
import time
from ast import literal_eval
from typing import Dict, List

import minimalmodbus
import pika
import constants


def connect_to_modbus(interface: str, address: int):
    """Подключиться к modbus с заданными параметрами."""
    try:
        instrument = minimalmodbus.Instrument(interface, address)
        instrument.serial.baudrate = constants.BAUDRATE
        instrument.serial.timeout = constants.TIMEOUT
        instrument.serial.parity = constants.PARITY
    except Exception:
        raise minimalmodbus.NoResponseError
    return instrument


def get_config_from_file() -> Dict:
    """Получить config устройства из файла по его имени."""
    try:
        with open(constants.DEVICE_CONFIG_FILE, 'r') as file:
            config_devices = json.load(file)
    except Exception:
        raise FileExistsError
    return config_devices


def write_to_modbus(device_config: Dict, value: str) -> None:
    """Передача данных через modbus в выбранное устройство."""
    try:
        instrument = connect_to_modbus(device_config.get('interface'),
                                       device_config.get('mb_address'))
        if instrument.serial.isOpen():
            instrument.write_register(
                registeraddress=device_config.get('slave_coil'),
                value=int(value),
                functioncode=device_config.get('function_code'),
            )
    except Exception as err:
        print(f"Can't connect to modbus address: {device_config.get('mb_address')} - {err}")


def callback(ch, method, properties, body):
    """Получение данных из очереди.
    Работа с ними в зависимости от типа устройства.
    """
    dictionary = json.loads(body.decode('utf-8'))
    # dictionary = literal_eval(string)
    device_config = devices_config.get(dictionary.get('slave_name'))
    if device_config and device_config.get('device_type') == 'executor':
        try:
            write_to_modbus(device_config, dictionary.get('value'))
        except Exception as err:
            print(f'WriteModbusError - {err}')
        else:
            if (dictionary.get('slave_name') not in executors_status_on
                    and int(dictionary.get('value')) == constants.HEX_ON):
                executors_status_on.append(dictionary.get('slave_name'))
                queue_to_logic.basic_publish(
                    exchange='',
                    routing_key='queue-logic',
                    body=json.dumps(executors_status_on).encode('utf-8')
                )
            elif (dictionary.get('slave_name') in executors_status_on
                  and int(dictionary.get('value')) == constants.HEX_OFF):
                executors_status_on.remove(dictionary.get('slave_name'))
                queue_to_logic.basic_publish(
                    exchange='',
                    routing_key='queue-logic',
                    body=json.dumps(executors_status_on).encode('utf-8')
                )
    else:
        print('device_config Empty')


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    queue_from_main = connection.channel()
    queue_from_main.queue_declare(queue='mb-queue-get')

    queue_to_logic = connection.channel()
    queue_to_logic.queue_declare(queue='queue-logic')

    try:
        devices_config = get_config_from_file()
    except FileExistsError as err:
        print(f'device_config ReadError - {err}')

    executors_status_on = ['executors']
    queue_from_main.basic_consume('mb-queue-get', callback, auto_ack=True)
    try:
        queue_from_main.start_consuming()
    except KeyboardInterrupt:
        queue_from_main.stop_consuming()
    finally:
        connection.close()
