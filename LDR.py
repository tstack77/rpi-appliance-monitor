#!/usr/bin/python
#Python application to send a Pushover message to be sent when an LDR sensor detects that an LED on a washer/dryer has turned off.
#Adapted from code written by Shmoopty, and others.

import RPi.GPIO as GPIO
import threading
import time
import sys
import requests
import httplib, urllib
from time import localtime, strftime
GPIO.setmode(GPIO.BCM)



# GPIO ## set up as input. See https://pinout.xyz/pinout/pin12_gpio18
sensor_GPIO = ##

#-------Pushover--------------------------------------------------#

# Setup pushover API. Register at https://pushover.net/
app_key = "***************"
user_key = "***************"
device = "***************"
#timestamp = 
#title = ""
#priority = ""
#sound = ""

# Message to be sent via Pushover. Ex= "Dry Cycle Complete"
PUSH_MSG = ""

#---------IFTTT---------------------------------------------------#

# Create a new Applet in IFTT with a Maker channel as the if
# Open the settings to the Maker Item, and navigate to the URL to get
# key.  Make a new activity with the Maker channel and use the event you
# define
maker_channel_key = "***************"
maker_channel_event = "***************"

#-----------------------------------------------------------------#

GPIO.setup(sensor_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
sensor_on = None
on = None
off = None
DELAY = 10

def sendPush(PUSH_MSG):
	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
		urllib.urlencode({
			"token": app_key,
			"user": user_key,
			"device": device,
			"message": PUSH_MSG,
			#"timestamp": 
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
	global on
	global off
	global sensor_on

	sensor_on = GPIO.input(sensor_GPIO)

	if (sensor_on):
		print 'Appliance OFF'
		off = "Appliance OFF"
	else:
		print 'Appliance ON'
		on = "Appliance ON"
		off = None

def heartbeat(*_):
        global on
        global off
	print 'HB'
	if (on != None and off != None):
		print (PUSH_MSG)
		sendPush(PUSH_MSG)
		iftt(PUSH_MSG)
		on = None
		off = None
		time.sleep(DELAY)

        threading.Timer(5, heartbeat).start()

GPIO.add_event_detect(sensor_GPIO, GPIO.BOTH, callback=sensor_switch)

print 'Monitoring GPIO pin {}'\
	.format(str(sensor_GPIO))
threading.Timer(5, heartbeat).start()