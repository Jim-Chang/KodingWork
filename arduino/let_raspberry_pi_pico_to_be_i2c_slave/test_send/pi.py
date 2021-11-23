import smbus

channel = 1
pico_addr = 0x50
reg_addr = 0x01

i2c_master = smbus.SMBus(channel)
data = i2c_master.read_word_data(pico_addr, reg_addr)
print('receive', data)