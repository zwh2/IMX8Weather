from smbus2 import SMBus
import time, json
from datetime import datetime


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
	#pass
    print (variable, '=', hex(eval(variable)))

if __name__ == "__main__":
	with SMBus(2) as bus:
		
		#init
		###light level sensor
		# make sure sensor is on, we are not worried about power consuption
		# ALS_GAIN: 1/8, ALS_IT 50
		bus.write_word_data(0x10, 0x00, 0x1200)
		
		###Pressure and temp
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
		#Reset Humidity
		bus.write_byte(0x40, 0xFE)
		## end initialization
	while(True):
		with SMBus(2) as bus:
			#start conversion for temp
			bus.write_byte(0x76, 0x50)
			# read humidity
			humidity = int.from_bytes(bytes(bus.read_i2c_block_data(0x40,0xE5,2)),'big')
			#read temp
			temp =bus.read_i2c_block_data(0x76,0x00,3)
			temp = int.from_bytes(bytes(temp),'big')
			#start conversion for pressure
			bus.write_byte(0x76, 0x40)
			# read from light sensor
			light = bus.read_word_data(0x10, 0x04)
			#read pressure
			pressure = int.from_bytes(bytes(bus.read_i2c_block_data(0x76,0x00,3)),'big')

		#Teperature/pressure calibration from data sheet 
		delta_temp = temp - (c5 << 8)
		initial_temp = float(2000) + (delta_temp * c6 >> 23)
		temp2, offset2, sensitivity2 = corrections(initial_temp, delta_temp)
		corrected_temp = (initial_temp -temp2) / 100
		offset = ((c2 << 17) + ((c4 *delta_temp) >> 6)) - offset2
		sensitivity = ((c1 << 16) +((c3*delta_temp) >> 7)) - sensitivity2
		corrected_pressure = ((((pressure *sensitivity) >>21) - offset) >> 15) / 100
		# print ("Corrected Temperature: ", corrected_temp, "C")
		# print ("Corrected Pressure: ", corrected_pressure, "mbar")
			
		#light level calibration
		corrected_light = light * 0.9216
		# print ("Corrected Light: ", round(corrected_light,0), "lx")

		#humidity calibration from data sheet
		corrected_humidity = (125 * humidity /(1 << 16))-6
		# print ("Corrected Humidity: ", round(corrected_humidity,1), '%')

		#time = str(datetime.now())
		data = {}
		data[str(datetime.now())]={
			'temp':corrected_temp,
			'pressure':round(corrected_pressure),
			'humidity':corrected_humidity,
			'light':corrected_light
		}
		# print (data)
		with open('/www/pages/live.json', 'w') as outfile:
			json.dump(data, outfile)
		
		time.sleep(1)

