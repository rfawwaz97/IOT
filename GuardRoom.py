# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
import Adafruit_DHT
import sys
import MFRC522
#from gpiozero import MCP3008

#adc = MCP3008(channel=0)
MIFAREReader = MFRC522.MFRC522()
pin = 4
# Custom MQTT message callback
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

my_rpi.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2) # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10) # 10 sec
my_rpi.configureMQTTOperationTimeout(5) # 5 sec

# Connect and subscribe to AWS IoT
my_rpi.connect()
my_rpi.subscribe("2M1C-Fawwaz/guardroom/sensors", 1, customCallback)
my_rpi.subscribe("2M1C-Fawwaz/guardroom/sensors", 1, customCallback)
my_rpi.subscribe("2M1C-Fawwaz/guardroom/sensors", 1, customCallback)
sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
#int humidity=0
#int temperature=0

while True:
	humidity, temperature = Adafruit_DHT.read_retry(11, pin)
	(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    	(status,uid) = MIFAREReader.MFRC522_Anticoll()
	userid = " "
	if status == MIFAREReader.MI_OK:
		(userid) = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
		print("UID:"+userid )
		if userid ==" ":
			userid = "0"
	my_rpi.publish("2M1C-Fawwaz/guardroom/sensors", int(temperature), 1)
	my_rpi.publish("2M1C-Fawwaz/guardroom/sensors", int(humidity), 1)
	my_rpi.publish("2M1C-Fawwaz/guardroom/sensors", str(userid), 1)
	loopCount = loopCount+1
    	message = {}
	#message1= {}
		#message1 = {}
    	message["deviceid"] = "deviceid_shakir"
    	import datetime as datetime
    	now = datetime.datetime.now()
    	message["datetimeid"] = now.isoformat()      
    	message["Temperature"] = temperature
    	message["Humidity"] = humidity
    	message["UserID"] = userid
    	import json
    	my_rpi.publish("2M1C-Fawwaz/guardroom/sensors", json.dumps(message), 1)
    	my_rpi.publish("2M1C-Fawwaz/guardroom/sensors", json.dumps(message), 1)
    	my_rpi.publish("2M1C-Fawwaz/guardroom/sensors", json.dumps(message), 1)

#light = round(1024-(adc.value*1024))
# my_rpi.publish("sensors/light", str(light), 1)
# sleep(5)
