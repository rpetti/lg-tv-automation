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
	sendCommand("ka 01 01\r")

def turnOffTv():
	sendCommand("ka 01 00\r")

def isPowerOn():
	resp = sendCommand("ka 01 FF\r")
	if resp == "a 01 OK00x":
		return False
	else:
		return True

def toggleTv():
	if isPowerOn():
		turnOffTv()
	else:
		turnOnTv()

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"h",["on","off","status"])
	except getopt.GetoptError:
		print 'tvpower.py [--on,--off,--status]'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'tvpower.py [--on,--off,--status]'
			sys.exit()
		if opt == "--on":
			print("turning on tv")
			turnOnTv()
		elif opt == "--off":
			print("turning off tv")
			turnOffTv()
		elif opt == "--status":
			print isPowerOn()

if __name__ == "__main__":
	main(sys.argv[1:])
	
