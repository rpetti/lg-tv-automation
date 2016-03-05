from flask import Flask

import tvpower
import wemo



app = Flask(__name__)

@app.route('/')
def index():
	return "<span style='color:red'>I am app 1</span>"

@app.route('/useTvForMediaCenter')
def useTvForMediaCenter():
	tvpower.turnOnTv()
	return "true"

@app.route('/dontUseTvForMediaCenter')
def dontUseTvForMediaCenter():
	tvpower.turnOffTv()
	return "true"

@app.route('/toggleLight')
def toggleLight():
	wemo.toggleLight()
	return "true"
