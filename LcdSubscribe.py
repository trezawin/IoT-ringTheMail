import time
from paho.mqtt.client import Client
from Lcd import Lcd

def on_message(c, userdata, mesg):
    print "message: %s %s %s" % (userdata, mesg.topic, mesg.payload)
    lcd = Lcd()
    lcd.clear()
    lcd.display_string(mesg.payload, 1)


client = Client(client_id="lcd", userdata="lcd")
client.connect("ringthemail.iot.sg")
client.on_message = on_message
client.subscribe("postBox1")
while True:
    client.loop()
    time.sleep(1)
