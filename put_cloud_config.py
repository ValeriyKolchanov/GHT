import json
from typing import Dict

CONFIG_FILE_NAME = 'cloud_config.json'

url = 'cloud.hightek.ru'
port = 1883
device_token = 'yN8DEeqWnR3e8nxcUAfe'


def get_base_json(cloud_url: str, cloud_port: int, device_token: str) -> Dict:
    """Собрать основные данные об облаке."""
    cloud = {
        'cloud_url': cloud_url,
        'cloud_port': cloud_port,
        'device_token': device_token,
    }
    return cloud


def write_json_file(settings: Dict) -> None:
    """Запись данных в JSON файл."""
    try:
        with open(CONFIG_FILE_NAME, 'w') as file:
            json.dump(settings, file)
    except IOError():
        print('File WriteError')


if __name__ == '__main__':
    settings = get_base_json(cloud_url=url, cloud_port=port,
                             device_token=device_token)
    write_json_file(settings=settings)
