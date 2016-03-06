#!/usr/bin/python

import ouimeaux
from ouimeaux.environment import Environment

def toggleLight():
	env = Environment()
	try:
		env.start()
	except:
		print "server may have been started already"
	for i in range(1,5):
		try:
			env.discover(i)
			switch = env.get_switch('WeMo Switch')
			switch.toggle()
		except:
			continue
		break

if __name__ == "__main__":
	toggleLight()
