import json
import time
from copy import deepcopy
from typing import Dict, List

import pika

import constants


def read_config_file(path: str) -> (Dict, List):
    """Чтение файла из заданной директории."""
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileExistsError:
        raise


def bool_logic_string(data: str) -> bool:
    """"""
    global executors_status

    def brackets_result(brackets: str) -> bool:
        i = 0
        result = []
        while i < len(brackets):
            if brackets[i] == '(':
                result.append('(')
                i += 1
            else:
                k = brackets.find(' ', i)
                if k == -1:
                    k = len(brackets)
                j = 1
                while not brackets[k - j].isalpha():
                    j += 1
                word = brackets[i:k - j + 1]
                if word.isupper():
                    logic_word = word.lower()
                    result.append(logic_word)
                else:
                    result.append(str(name in executors_status))
                if j > 1:
                    result.append(')' * (j - 1))
                i = k + 1
        print(result)
        return eval(' '.join(result))

    marker = data.find(' ')
    if marker == -1:
        name, status = data.split('_')
        all_result = (status == 'ON' and name not in executors_status or
                      status == 'OFF' and name in executors_status)
    else:
        name, status = data[:marker].split('_')
        brackets_bool_result = brackets_result(data[marker + 2:-1])
        slave_result = (status == 'ON' and name not in executors_status or
                        status == 'OFF' and name in executors_status)
        all_result = slave_result and brackets_bool_result
    return all_result


def callback(ch, method, properties, body):
    """"""
    global executors_status, sensors_status

    data = json.loads(body.decode('utf-8'))
    if data[0] == 'sensors':
        del sensors_status[0]
        del data[0]
        sensors_status.append(data)
    elif data[0] == 'executors':
        del data[0]
        executors_status = deepcopy(data)
    elif data[0] == 'timers':
        if data[2] == constants.HEX_ON:
            device_logic = logic_rules.get(data[1]['ON'])
        elif data[2] == constants.HEX_OFF:
            device_logic = logic_rules.get(data[1]['OFF'])
        bool_device_logic = bool_logic_string(device_logic)
        if bool_device_logic:
            body = {'slave_name': data[1], 'value': data[2]}
            queue_to_main.basic_publish(
                exchange='',
                routing_key='mb-queue-get',
                body=json.dumps(body).encode('utf-8')
            )


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost', blocked_connection_timeout=0.5))
    queue_to_main = connection.channel()
    queue_to_main.queue_declare(queue='mb-queue-get')

    queue_to_logic = connection.channel()
    queue_to_logic.queue_declare(queue='queue-logic')
    queue_to_logic.basic_consume('queue-logic', callback, auto_ack=True)

    logic_rules = read_config_file(constants.DECISION_LOGIC_FILE)
    executors_status = []
    sensors_status = [None] * constants.SENSORS_LIST_LENGTH
    try:
        queue_to_logic.start_consuming()
    except (KeyboardInterrupt, SystemExit):
        queue_to_logic.stop_consuming()
    finally:
        connection.close()
