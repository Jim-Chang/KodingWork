from i2c_responder import I2CResponder

channel = 0
sda_pin = 4
scl_pin = 5
addr = 0x50

i2c_slave = I2CResponder(channel, sda_pin, scl_pin, addr)

def check_if_need_response():
    if i2c_slave.read_is_pending():
        i2c_slave.put_read_data(0xFF)

def check_receive():
    data = []
    while i2c_slave.write_data_is_available():
        data += i2c_slave.get_write_data(50)
    print('receive data', data)

while True:
    check_receive()
    check_if_need_response()