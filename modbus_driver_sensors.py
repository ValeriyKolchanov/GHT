import json
import time
from typing import List

import minimalmodbus
import pika
import serial

BAUDRATE = 9600
TIMEOUT = 0.2
PARITY = serial.PARITY_NONE
DEVICE_CONFIG_FILE = '../configs/device_config.json'
UPDATE_SENSORS_STATUS = 30


def connect_to_modbus(interface: str, address: int):
    try:
        instrument = minimalmodbus.Instrument(interface, address)
        instrument.serial.baudrate = BAUDRATE
        instrument.serial.timeout = TIMEOUT
        instrument.serial.parity = PARITY
    except minimalmodbus.NoResponseError:
        raise
    return instrument


def check_sensors_status() -> List:
    """
    Считывает данные с устройств типа sensor.
    Возвращает данные в список.
    """
    try:
        with open(DEVICE_CONFIG_FILE, 'r') as file:
            config_devices = json.load(file)
    except FileExistsError:
        raise

    result = ['sensors']
    for device in config_devices.values():
        if device.get('device_type') == 'sensor':
            try:
                instrument = connect_to_modbus(device.get('interface'),
                                               device.get('mb_address'))
                if instrument.serial.isOpen():
                    value = instrument.read_register(
                        registeraddress=device.get('slave_coil'),
                        number_of_decimals=device.get('slave_decimals'),
                        functioncode=device.get('function_code')
                    )
                else:
                    value = None
                time.sleep(0.5)
            except Exception as err:
                print(f"Can't read sensor {device.get('slave_name')} - error {err}")
                value = None
            finally:
                result.append({device.get('slave_name'): value})
    return result


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    queue_to_main = connection.channel()
    queue_to_main.queue_declare(queue='mb-queue-put')

    queue_to_logic = connection.channel()
    queue_to_logic.queue_declare(queue='queue-logic')

    add_list = []
    try:
        while True:
            try:
                body = check_sensors_status()
                queue_to_main.basic_publish(
                    exchange='',
                    routing_key='mb-queue-put',
                    body=json.dumps(body).encode('utf-8')
                )
                body.insert(0, 'sensors')
                queue_to_logic.basic_publish(
                    exchange='',
                    routing_key='queue-logic',
                    body=json.dumps(body).encode('utf-8')
                )
            except FileExistsError as err:
                print(f'FileRead Error - {err}')
            finally:
                time.sleep(UPDATE_SENSORS_STATUS)
    except KeyboardInterrupt:
        connection.close()
        raise
