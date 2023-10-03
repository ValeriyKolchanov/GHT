import json
from datetime import datetime
from typing import Dict, List

import pika
from apscheduler.schedulers.background import BlockingScheduler

import constants


def read_config_file(path: str) -> (Dict, List):
    """Чтение файла из заданной директории."""
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileExistsError:
        raise


def check_slaves_on(slave_name):
    """Передача в очередь команды на включение устройства."""
    body = json.dumps(['timers', slave_name, constants.HEX_ON])
    queue_to_logic.basic_publish('', 'queue-logic', body.encode('utf-8'))


def check_slaves_off(slave_name):
    """Передача в очередь команды на выключение устройства."""
    body = json.dumps(['timers', slave_name, constants.HEX_OFF])
    queue_to_logic.basic_publish('', 'queue-logic', body.encode('utf-8'))


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost', blocked_connection_timeout=0.5))
    queue_to_logic = connection.channel()
    queue_to_logic.queue_declare(queue='queue-logic')

    devices_config = read_config_file(constants.DECISION_TIMERS_FILE)

    job_defaults = {'coalesce': False, 'max_instances': 2}
    scheduler = BlockingScheduler(job_defaults=job_defaults)

    for device_name, device_config in devices_config.items():
        if device_config.get('type') == 'timer':
            scheduler.add_job(
                check_slaves_on,
                'cron',
                args=(device_name,),
                hour=device_config.get('on')[0],
                minute=device_config.get('on')[1],
                jitter=30
            )
            scheduler.add_job(
                check_slaves_off,
                'cron',
                args=(device_name,),
                hour=device_config.get('off')[0],
                minute=device_config.get('off')[1],
                jitter=30
            )
        elif device_config.get('type') == 'period':
            start_date = datetime.fromtimestamp(
                datetime.now().timestamp()
                + device_config.get('delta')
                + device_config.get('duration')
            )
            scheduler.add_job(
                check_slaves_on,
                'interval',
                args=(device_name,),
                seconds=device_config.get('delta'),
                jitter=10
            )
            scheduler.add_job(
                check_slaves_off,
                'interval',
                args=(device_name,),
                start_date=start_date,
                seconds=device_config.get('delta'),
                jitter=10
            )
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
