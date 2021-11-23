import smbus

channel = 1
pico_addr = 0x50
reg_addr = 0x01

i2c_master = smbus.SMBus(channel)
i2c_master.write_block_data(pico_addr, reg_addr, [0x30, 0x40, 0x50])