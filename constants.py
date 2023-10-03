import serial

SENSORS_LIST_LENGTH = 3
DECISION_TIMERS_FILE = '../configs/decisions_timers_config.json'
DECISION_LOGIC_FILE = '../configs/decisions_logic_config.json'
DEVICE_CONFIG_FILE = '../configs/device_config.json'

UPDATE_SENSORS_STATUS = 30
HEX_ON = 256
HEX_OFF = 512
BAUDRATE = 9600
TIMEOUT = 0.2
PARITY = serial.PARITY_NONE
