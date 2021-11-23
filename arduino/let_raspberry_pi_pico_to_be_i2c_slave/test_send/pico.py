from i2c_responder import I2CResponder

channel = 0
sda_pin = 4
scl_pin = 5
addr = 0x50

i2c_slave = I2CResponder(channel, sda_pin, scl_pin, addr)

while True:
    if i2c_slave.read_is_pending():
        i2c_slave.put_read_data(0xFF)