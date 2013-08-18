#!/usr/bin/python

import serial
import socket
from scapy.all import *
import time
import BaseHTTPServer
import thread
from threading import Lock

HOST_NAME='192.168.1.21'
PORT_NUMBER=8798

class SharedData():
	__data = {}
	__lock = Lock()

	@classmethod
	def set(cls, name, value):
		with cls.__lock:
			cls.__data[name] = value
	@classmethod
	def get(cls, name):
		with cls.__lock:
			return cls.__data[name]

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_POST(s):
		print(s.path)
		if s.path == '/useTvForMediaCenter':
			SharedData.set('useTvForMediaCenter',True)
			print('use tv for media center')
		if s.path == '/dontUseTvForMediaCenter':
			SharedData.set('useTvForMediaCenter',False)
			print('dont use tv for media center')
		s.send_response(200)
		s.send_header('Content-type','text/html')
		s.end_headers()
		s.wfile.write('<html><body>Ok</body></html>')

def httpListenerThread():
	server_address=(HOST_NAME,PORT_NUMBER)
	httpd = BaseHTTPServer.HTTPServer(server_address,MyHandler)
	httpd.serve_forever()

httpListenerThread = thread.start_new_thread(httpListenerThread,())

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

usingTvWithXbox=False
usingTvWithMediaCenter=False
tvOn=False
SharedData.set('useTvForMediaCenter',False)

while(True):
	useTvForMediaCenter = SharedData.get('useTvForMediaCenter')
	if isXboxOn():
		if not usingTvWithXbox:
			if not isTvOn():
				turnOnTv()
			tvOn=True
			switchToXbox()
			usingTvWithXbox=True
	else:
		if usingTvWithXbox:
			switchToMediaCenter()
			usingTvWithXbox=False

	if useTvForMediaCenter:
		if not usingTvWithMediaCenter:
			if not isTvOn():
				turnOnTv()
			tvOn=True
			switchToMediaCenter()
			usingTvWithMediaCenter=True
	else:
		if usingTvWithMediaCenter:
			usingTvWithMediaCenter=False
	if (not usingTvWithMediaCenter) and (not usingTvWithXbox):
		if tvOn==True:
			turnOffTv()
			tvOn=False
	time.sleep(5)
