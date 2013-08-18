#!/usr/bin/python

import serial
import socket
from scapy.all import *
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
	time.sleep(10)

def turnOffTv():
	print("turning off tv")
	sendCommand("ka 01 00\r")
	time.sleep(10)

def switchToXbox():
	print("switching to xbox input")
	sendCommand("kb 01 08\r")
	time.sleep(5)

def switchToMediaCenter():
	print("switching to mediacenter input")
	sendCommand("kb 01 07\r")
	time.sleep(5)

def isTvOn():
	resp = sendCommand("ka 01 ff\r")
	if resp == 'a 01 OK01x':
		return True
	else:
		return False
	time.sleep(2)

def isXboxOn_Scapy():
	response = sr1(IP(dst='xbox360')/TCP(dport=1025,flags="S"),verbose=False,timeout=0.2)
	if response:
		if response[TCP].flags == 18:
			return True
	return False

def isXboxOn_Scapy_ARP():
	conf.verb=0
	ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.23"),timeout=2)
	for snd,rcv in ans:
		return True
	return False

def isXboxOn_Connect():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(5)
	result=1
	try:
		result = s.connect(('xbox360',1025))
	except:	pass
	if result == 0:
		return True
	s.close()
	return False

def isXboxOn():
	return isXboxOn_Scapy_ARP()

xboxOn=False
turnTvOffWithXbox=False


while(True):
	if isXboxOn():
		if not xboxOn:
			if not isTvOn():
				turnOnTv()
				turnTvOffWithXbox=True
			switchToXbox()
			xboxOn=True
	else:
		if xboxOn:
			switchToMediaCenter()
			if turnTvOffWithXbox:
				turnOffTv()
				turnTvOffWithXbox=False
		xboxOn=False
	time.sleep(5)
