from i2c_responder import I2CResponder

channel = 0
sda_pin = 4
scl_pin = 5
addr = 0x50

i2c_slave = I2CResponder(channel, sda_pin, scl_pin, addr)

while True:
    data = []

    while i2c_slave.write_data_is_available():
        data += i2c_slave.get_write_data(50)

    print('receive data', data)