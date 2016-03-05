#!/usr/bin/python

import ouimeaux
from ouimeaux.environment import Environment

def toggleLight():
	env = Environment()
	try:
		env.start()
	except:
		print "server may have been started already"
	env.discover(3)
	switch = env.get_switch('WeMo Switch')
	switch.toggle()

if __name__ == "__main__":
	toggleLight()
