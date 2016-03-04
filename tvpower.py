#!/usr/bin/python

import serial
import getopt
import sys
import time

def sendCommand(cmd):
	ser = serial.Serial(
		port='/dev/ttyUSB0',
		baudrate=9600,
		parity='N',
		stopbits=1,
		bytesize=8)
	ser.write(cmd)
	response = ser.read(10)
	return response
	ser.close()

def turnOnTv():
	print("turning on tv")
	sendCommand("ka 01 01\r")
	time.sleep(1)

def turnOffTv():
	print("turning off tv")
	sendCommand("ka 01 00\r")
	time.sleep(1)

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"h",["on","off"])
	except getopt.GetoptError:
		print 'tvpower.py [--on,--off]'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'tvpower.py [--on,--off]'
			sys.exit()
		if opt == "--on":
			turnOnTv()
		elif opt == "--off":
			turnOffTv()

if __name__ == "__main__":
	main(sys.argv[1:])
	
