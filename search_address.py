import minimalmodbus
import serial

BAUDRATE = 9600
TIMEOUT = 0.2
PARITY = serial.PARITY_NONE

for i in range(250):
    try:
        instrument = minimalmodbus.Instrument('COM3', i)
        instrument.serial.baudrate = BAUDRATE
        instrument.serial.timeout = TIMEOUT
        instrument.serial.parity = PARITY
        value = instrument.read_register(0x0001, number_of_decimals=1, functioncode=0x04)
        print(f'temperature - {value}, address - {i}')
    except Exception:
        print(f'address {i} not exist')
