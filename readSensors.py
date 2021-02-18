from smbus2 import SMBus
import time



#borrowed from Adafruit driver
def corrections(initial_temp, delta_temp):
	# # Second order temperature compensation
	if initial_temp < 2000:
		delta_2k = initial_temp - 2000
		temp_factor = delta_2k ** 2 >> 4
		temp2 = (3 * delta_temp ** 2) >> 33
		offset2 = 61 * temp_factor
		sensitivity2 = 29 * temp_factor

		if initial_temp < -1500:
			delta_15k = initial_temp + 1500
			temp_factor = delta_15k ** 2

			offset2 += 17 * temp_factor
			sensitivity2 += 9 * temp_factor
		#
	else:
		temp2 = (5 * delta_temp ** 2) >> 38
		offset2 = 0
		sensitivity2 = 0
	return temp2, offset2, sensitivity2

#debug function
def debug(variable):
	pass
    #print (variable, '=', (eval(variable)))

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
	c0 = int.from_bytes(bytes(bus.read_i2c_block_data(0x76 , 0xA0, 2)), 'big')
	c1 = int.from_bytes(bytes(bus.read_i2c_block_data(0x76 , 0xA2, 2)), 'big')
	c2 = int.from_bytes(bytes(bus.read_i2c_block_data(0x76 , 0xA4, 2)), 'big')
	c3 = int.from_bytes(bytes(bus.read_i2c_block_data(0x76 , 0xA6, 2)), 'big')
	c4 = int.from_bytes(bytes(bus.read_i2c_block_data(0x76 , 0xA8, 2)), 'big')
	c5 = int.from_bytes(bytes(bus.read_i2c_block_data(0x76 , 0xAA, 2)), 'big')
	c6 = int.from_bytes(bytes(bus.read_i2c_block_data(0x76 , 0xAC, 2)), 'big')
	debug('c0')
	debug('c1')
	debug('c2')
	debug('c3')
	debug('c4')
	debug('c5')
	debug('c6')

	#start conversion for temp
	bus.write_byte(0x76, 0x50)
	#wait for conversion to complete
	time.sleep(0.001)
	#read temp
	temp =bus.read_i2c_block_data(0x76,0x00,3)
	temp = int.from_bytes(bytes(temp),'big')
	#print ("uncorrected temperature is: ",temp)
	
	#start conversion for pressure
	bus.write_byte(0x76, 0x40)
	#wait for conversion to complete
	time.sleep(0.001)
	#read pressure
	pressure = int.from_bytes(bytes(bus.read_i2c_block_data(0x76,0x00,3)),'big')
	#print ("uncorrected pressure is: ", pressure)

	#Teperature/pressure calibration from data sheet 
	delta_temp = temp - (c5 << 8)
	debug('delta_temp')
	initial_temp = float(2000) + (delta_temp * c6 >> 23)
	debug('initial_temp')
	temp2, offset2, sensitivity2 = corrections(initial_temp, delta_temp)
	corrected_temp = (initial_temp -temp2) / 100
	offset = ((c2 << 17) + ((c4 *delta_temp) >> 6)) - offset2
	debug('offset')
	sensitivity = ((c1 << 16) +((c3*delta_temp) >> 7)) - sensitivity2
	debug('sensitivity')
	corrected_pressure = ((((pressure *sensitivity) >>21) - offset) >> 15) / 100
	print ("Corrected Temperature: ", corrected_temp, "C")
	print ("Corrected Pressure: ", corrected_pressure, "mbar")
	
	
