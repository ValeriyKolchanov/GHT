import json
from typing import Dict

device_id = 8
module_name = 'Relay'
interface = '/dev/ttyUSB0'
device_type = 'executor'
mb_address = 23
function_code = 0x06
slave_coil = 0x0015
slave_decimals = 0
slave_name = 'Relay-15'
slave_type = 'light'


def get_base_json(id: int, module_name: str, interface: str, type :str,
                  mb_address: int, function_code: int,
                  slave_coil: int, slave_decimals: int,
                  slave_name: str, slave_type: str) -> Dict:
    """Собрать основные данные об устройстве."""
    device = {
        'id': id,
        'module_name': module_name,
        'interface': interface,
        'device_type': type,
        'mb_address': mb_address,
        'function_code': function_code,
        'slave_name': slave_name,
        'slave_decimals': slave_decimals,
        'slave_coil': slave_coil,
        'slave_type': slave_type,
        }
    return device


def is_file_not_empty() -> bool:
    """Проверить файл на наличие данных."""
    try:
        with open('device_config.json', 'r') as file:
            check = file.read()
    except IOError():
        print('File ReadError')
    return bool(check)


def read_json_file(device: Dict) -> Dict:
    """Чтение данных из JSON файла. Если файл пуст, создать новый словарь."""
    if is_file_not_empty():
        try:
            with open('device_config.json', 'r') as file:
                devices = json.load(file)
            devices[device['slave_name']] = device
            return devices
        except IOError():
            print('File ReadError')
    return {device['slave_name']: device}


def write_json_file(devices: Dict) -> None:
    """Запись данных в JSON файл."""
    try:
        with open('device_config.json', 'w') as file:
            json.dump(devices, file)
    except IOError():
        print('File WriteError')


if __name__ == '__main__':
    device = get_base_json(id=device_id, module_name=module_name,
                           interface=interface, mb_address=mb_address,
                           type=device_type, slave_coil=slave_coil,
                           slave_decimals=slave_decimals, function_code=function_code,
                           slave_name=slave_name, slave_type=slave_type)
    devices = read_json_file(device=device)
    write_json_file(devices=devices)
