#!/usr/bin/python
#Python application for rpi to send a Pushover message when an LDR sensor detects that an LED on a washer/dryer has turned off.
#Adapted from code written by Shmoopty, and others.

import RPi.GPIO as GPIO
import threading
import time
import sys
import requests
import httplib, urllib
from time import localtime, strftime

# Setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

# GPIO ## set up as input. See https://pinout.xyz/pinout/pin12_gpio18
sensor_GPIO = ##
GPIO.setup(sensor_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


#-------Pushover--------------------------------------------------#

# Setup pushover API. Register at https://pushover.net/
app_key = "************"
user_key = "************"
device = "************"
#title = ""
#priority = ""
#sound = ""

# Message to be sent via Pushover. Ex = "Wash Cycle Complete"
PUSH_MSG = ""

#---------IFTTT---------------------------------------------------#

# Create a new Applet in IFTT with a Maker channel as the if
# Open the settings to the Maker Item, and navigate to the URL to get
# key.  Make a new activity with the Maker channel and use the event you
# define
maker_channel_key = "************"
maker_channel_event = "************"


#_________________________________________________________________#

sensor_on = None
last_signal_on_time = None
last_signal_off_time = None

# This function sends the push message using Pushover.
def sendPush(PUSH_MSG):
	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
		urllib.urlencode({
			"token": app_key,
			"user": user_key,
			"device": device,
			"message": PUSH_MSG, 
			#"title": 
			#"priority": 
			#"sound": 
		}), { "Content-type": "application/x-www-form-urlencoded" })

	conn.getresponse()
	return

def iftt(PUSH_MSG):
		iftt_url = "https://maker.ifttt.com/trigger/{}/with/key/{}".format(maker_channel_event, maker_channel_key)
		report = {"value1" : PUSH_MSG}
		resp = requests.post(iftt_url, data=report)
	
def sensor_switch(*_):
	global last_signal_on_time
	global last_signal_off_time
	global sensor_on
	print 'HB'

	sensor_on = GPIO.input(sensor_GPIO)

	if (sensor_on):
		print 'Machine OFF', time.strftime("%H%M%S")
		last_signal_off_time = time.time()
	else:
		print 'Machine ON', time.strftime("%H%M%S")
		last_signal_on_time = time.time()

	if (last_signal_on_time != None and last_signal_off_time > last_signal_on_time):
		print (PUSH_MSG)
		sendPush(PUSH_MSG)
		iftt(PUSH_MSG)
		print 'last signal on', last_signal_on_time
		print 'last signal off', last_signal_off_time
		last_signal_on_time = None
		last_signal_off_time = None

	threading.Timer(10, sensor_switch).start()

GPIO.add_event_detect(sensor_GPIO, GPIO.BOTH, callback=sensor_switch)

print 'Monitoring GPIO pin {}'\
	.format(str(sensor_GPIO))
threading.Timer(1, sensor_switch).start()
