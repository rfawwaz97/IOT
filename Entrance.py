# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from gpiozero import MCP3008, MotionSensor, LED
from time import time, sleep
from twilio.rest import Client
import datetime
from picamera import PiCamera

adc = MCP3008(channel=0)
pir = MotionSensor(26, sample_rate=5,queue_len=1)
ledRed = LED(5)
camera = PiCamera()
# Twilio----------------------------------------------

account_sid = "ACd79c4e1721ccf1ac17b0d27ebd7d10d1"
auth_token = "60b19c5b631ec1b5354b762138a42126"
client = Client(account_sid, auth_token)

my_hp = "+6587540499"
twilio_hp = "+13168359808"


# Custom MQTT message callback------------------------
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

# AWS Certs-------------------------------------------	
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

# Connect and subscribe to AWS IoT---------------------
my_rpi.connect()
my_rpi.subscribe("2M1C-Fawwaz/entrance/sensors", 1, customCallback)
sleep(5)

# Publish to the same topic in a loop forever----------
loopCount = 0
while True:
	light = round(1024-(adc.value*1024))
	motionTrue = "Motion Detected"
	motionFalse = "No Motion Detected"
	camOn= "Camera is On"
	camOff= "Camera is Off"
	loopCount = loopCount+1
	message = {}
	message["deviceid"] = "deviceid_fawwaz"
	today = datetime.datetime.now()
	message["datetimeid"] = today.isoformat()      


	# Send Twilio SMS
	old_time = time()
	pir.wait_for_motion()
	new_time = time()

	# If light value is less than 600, do...
	if light < 600:
		#If motion is detected..
		if new_time - old_time > 1:        
			ledRed.on()
			print("Begin video recording!")
			camera.start_recording('/home/pi/Desktop/VidFolder/'+str(today)+'.h264')
			camera.wait_recording(20)
			camera.stop_recording()
			print("Video recording ended!")
			print("Sending SMS to user\n\n")
			sms = "Motion Detected On " + str(today)
			message = client.api.account.messages.create(to=my_hp,from_=twilio_hp,body=sms)
			message["Light"] = light
			message["Motion"] = motionTrue
			message["CamStatus"] = camOn
			import json
			my_rpi.publish("2M1C-Fawwaz/entrance/sensors", json.dumps(message), 1)
			ledRed.off()
			sleep(5)
		#If no motion....
		else:
			old_time = new_time
			pir.wait_for_no_motion()
			new_time = time()
			message["Light"] = light
			message["Motion"] = motionFalse
			message["CamStatus"] = camOn
			import json
			my_rpi.publish("2M1C-Fawwaz/entrance/sensors", json.dumps(message), 1)
			sleep(5)
	#Else...
	else:
		message["Light"] = light
		message["Motion"] = "N/A"
		message["CamStatus"] = camOff
		import json
		my_rpi.publish("2M1C-Fawwaz/entrance/sensors", json.dumps(message), 1)
		sleep(5)
	
	
