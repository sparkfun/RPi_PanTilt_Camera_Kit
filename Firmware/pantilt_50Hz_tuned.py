## Modified by: Wes @ SparkFun
## Written by: Mike Hord @ SparkFun

## Modified example code for 50Hz and calibrated with servo using an oscilloscope.

#!/usr/bin/env python

import smbus
import time

bus = smbus.SMBus(1)
addr = 0x40

def scale(x, in_min, in_max, out_min, out_max):
	return (x - in_min)*(out_max - out_min)/(in_max - in_min) + out_min

## enable the PC9685 and enable autoincrement

bus.write_byte_data(addr, 0, 0x20) # enable the chip
time.sleep(.1)
bus.write_byte_data(addr, 0, 0x10) # enable Prescale change as noted in the datasheet
time.sleep(.1) # delay for reset
bus.write_byte_data(addr, 0xfe, 0x88) #changes the Prescale register value for 50 Hz, using the equation in the datasheet (I later adjusted the value to fine tune the signal with an oscilloscope. The original value was 0x79.)
time.sleep(.1)
bus.write_byte_data(addr, 0, 0x20) # enables the chip

time.sleep(.1)
bus.write_word_data(addr, 0x06, 0) # chl 0 start time = 0us
bus.write_word_data(addr, 0x08, 350) # chl 0 end time = 1.5ms (I later adjusted the value to fine tune it to the servo I was testing with. The original value was 312.)

bus.write_word_data(addr, 0x0a, 0) # chl 1 start time = 0us
bus.write_word_data(addr, 0x0c, 350) # chl 1 end time = 1.5ms (I later adjusted the value to fine tune it to the servo I was testing with. The original value was 312.)

while True:
	pipein = open("/var/www/html/FIFO_pipan", 'r')
	line = pipein.readline()
	line_array = line.split(' ')
	if line_array[0] == "servo":
		pan_setting = scale(int(line_array[1]), 80, 220, 250, 440) # I later adjusted the value to fine tune it to the servo I was testing with. The original position values were 209 and 416.
		tilt_setting = scale(int(line_array[2]), 50, 250, 250, 440) # I later adjusted the value to fine tune it to the servo I was testing with. The original position values were 209 and 416.
		bus.write_word_data(addr, 0x08, pan_setting)
		bus.write_word_data(addr, 0x0c, tilt_setting)
pipein.close()
