# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
import Adafruit_DHT
import sys
from time import time
from gpiozero import MotionSensor
import datetime
pir = MotionSensor(26, sample_rate=5,queue_len=1)
#from gpiozero import MCP3008

from twilio.rest import Client
from gpiozero import LED, Button
from rpi_lcd import LCD #\\ used for lcd 
#----------------------------------------------------
#Twilio and LCD
lcd = LCD()
account_sid = "AC8c11af0109a45b1016069562126dd605"
auth_token = "38d5f83ab73dc1c75e93a0db9a87d784"
client = Client(account_sid, auth_token)
my_hp = "+6591138883"
twilio_hp = "+14244002037"

#----------------------------------------------------

led = LED(18)

pin = 4

def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")
	
host = "abpl27ba00qyj-ats.iot.us-west-2.amazonaws.com"
rootCAPath = "AmazonRootCA1.pem"
certificatePath = "cd5aee883b-certificate.pem.crt"
privateKeyPath = "cd5aee883b-private.pem.key"

my_rpi = AWSIoTMQTTClient("2M1C-Fawwaz-basicPubSub")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
my_rpi.connect()
my_rpi.subscribe("2M1C-Fawwaz/RestrictedArea/sensors", 1, customCallback)
my_rpi.subscribe("2M1C-Fawwaz/RestrictedArea/sensors", 1, customCallback)
my_rpi.subscribe("2M1C-Fawwaz/RestrictedArea/sensors", 1, customCallback)

sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, pin)
    my_rpi.publish("2M1C-Fawwaz/RestrictedArea/sensors", int(temperature), 1)
    my_rpi.publish("2M1C-Fawwaz/RestrictedArea/sensors", int(humidity), 1)


    old_time = time()
    pir.wait_for_motion()
    new_time = time()
    today = datetime.datetime.now()

    if new_time - old_time > 1:
        sms = "Potential Outbreak Detected at " + str(today)
        my_rpi.publish("2M1C-Fawwaz/RestrictedArea/sensors", str(sms), 1)
        #sms = "Potential Outbreak Detected at " + str(today) #uncomment this and the bottom when finialize with the codes
        #message = client.api.account.messages.create(to=my_hp,from_=twilio_hp,body=sms) 
        led.on()
        lcd.text("Potential OutBreak ", 1) #\\will show the temp on the top line 
        lcd.text('Detected!', 2) #\\ will show the humidity on the second line 
        sleep(3)
    else:
        sms = "No Motion Detected"
        sleep(3)

    loopCount = loopCount+1
    message = {}
    message1 = {}

    message["deviceid"] = "deviceid_zongbei"
    import datetime as datetime
    now = datetime.datetime.now()
    message["datetimeid"] = now.isoformat()      
    message["Humidity"] = humidity
    message["Temperature"] = temperature
    message["Message"] = sms
    
    
    

    import json
    my_rpi.publish("2M1C-Fawwaz/RestrictedArea/sensors", json.dumps(message), 1)
    my_rpi.publish("2M1C-Fawwaz/RestrictedArea/sensors", json.dumps(message), 1)
    my_rpi.publish("2M1C-Fawwaz/RestrictedArea/sensors", json.dumps(message), 1)


        
        
        

    #light = round(1024-(adc.value*1024))
     #   my_rpi.publish("sensors/light", str(light), 1)
    #    sleep(5)


        