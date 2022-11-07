import paho.mqtt.client as mqtt
import uuid
import qwiic_joystick
import time
import sys
import json

# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

while True:
    cmd = "an464vip6/joystick"
    topic = f"IDD/{cmd}"
    
    myJoystick = qwiic_joystick.QwiicJoystick()
    if myJoystick.connected == False:
        print("The Qwiic Joystick device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
    
    else:
        myJoystick.begin()
        x = myJoystick.horizontal
        y = myJoystick.vertical
        button = myJoystick.button
        val = str({"x": x, "y": y, "button": button})
        client.publish(topic, val)
        print(val)
    
    time.sleep(0.05)