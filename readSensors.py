from smbus2 import SMBus
import time

with SMBus(2) as bus:
		
	#light level sensor
	# make sure sensor is on, we are not worried about power consuption
	bus.write_word_data(0x10, 0x00, 0x1000)
	time.sleep(0.01)
	# read from light sensor
	light = bus.read_word_data(0x10, 0x04)
	print ("light level is: ", light)
		
	#Pressure and temp
	#reset device
	bus.write_byte(0x76 , 0x1E)
	#read the calibration data	
	c1 = bus.read_word_data(0x10, 0xA2)
	c2 = bus.read_word_data(0x10, 0xA4)
	c3 = bus.read_word_data(0x10, 0xA6)
	c4 = bus.read_word_data(0x10, 0xA8)
	c5 = bus.read_word_data(0x10, 0xAA)
	c6 = bus.read_word_data(0x10, 0xAC)
	#start conversion for temp
	bus.write_byte(0x76, 0x50)
	#wait for conversion to complete
	time.sleep(0.001)
	#read temp
	temp =bus.read_i2c_block_data(0x76,0x00,3)
	temp = int.from_bytes(bytes(temp),'big')
	print ("uncorrected temperature is: ",temp)
	
	#start conversion for pressure
	bus.write_byte(0x76, 0x40)
	#wait for conversion to complete
	time.sleep(0.001)
	#read pressure
	pressure = int.from_bytes(bytes(bus.read_i2c_block_data(0x76,0x00,3)),'big')
	print ("uncorrected pressure is: ", pressure)

	#Teperature calibration
	
