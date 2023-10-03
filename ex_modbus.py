import minimalmodbus
import serial
import time

BAUDRATE = 9600
TIMEOUT = 0.2
PARITY = serial.PARITY_NONE

# current_time = time.time()
relay = minimalmodbus.Instrument('/dev/ttyUSB0', 23)
relay.serial.baudrate = BAUDRATE
relay.serial.timeout = TIMEOUT
relay.serial.parity = PARITY

# sensor = minimalmodbus.Instrument('COM4', 80)
# sensor.serial.baudrate = BAUDRATE
# sensor.serial.timeout = TIMEOUT
# sensor.serial.parity = PARITY

# value = instrument.read_register(0x0001, number_of_decimals=1, functioncode=0x04)
# print(value)
# print(time.time() - current_time)
while True:
    coil = int(input('Coil: '))
    command = int(input('Command: '))
    relay.write_register(coil, command, functioncode=0x06)
    print(f'Coil - {coil}, Command - {command}')
