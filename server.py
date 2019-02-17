from flask import Flask, render_template, jsonify,request

app = Flask(__name__)
import sys  
import dynamodb1
import dynamodb2
import dynamodb3
import jsonconverter as jsonc
from gpiozero import LED
Led1 = LED (18)
Led2 = LED (5)
Led3 = LED (16)
#===========================================================================================================================

def led1On():
	Led1.blink()
	return "Entrance Red has been turned On"

def led1Off():
	Led1.off()
	return "Entrance Red has been turned Off"
  
def led2On():
	Led2.on()
	return "Wide Light has been turned On"

def led2Off():
	Led2.off()
	return "Wide Light has been turned Off"

def led3On():
	Led3.on()
	return "Lockdown has been turned On"

def led3Off():
	Led3.off()
	return "Lockdown has been turned Off"
	
def ledStatus():
	if led.is_lit:
		return 'On'
	else:
		return 'Off'
#===========================================================================================================================
@app.route("/api/getdata1",methods=['POST','GET'])
def apidata_getdata1():
    if request.method == 'POST' or request.method == 'GET':
        try:
            data = {'chart_data': jsonc.data_to_json(dynamodb1.get_data_from_dynamodb()), 'title': "IOT Data"}
            return jsonify(data)

        except:
            import sys
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

@app.route("/api/getdata2",methods=['POST','GET'])
def apidata_getdata2():
    if request.method == 'POST' or request.method == 'GET':
        try:
            data = {'chart_data': jsonc.data_to_json(dynamodb2.get_data_from_dynamodb()), 'title': "IOT Data"}
            return jsonify(data)

        except:
            import sys
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

@app.route("/api/getdata3",methods=['POST','GET'])
def apidata_getdata3():
    if request.method == 'POST' or request.method == 'GET':
        try:
            data = {'chart_data': jsonc.data_to_json(dynamodb3.get_data_from_dynamodb()), 'title': "IOT Data"}
            return jsonify(data)

        except:
            import sys
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/RestrictedArea")
def RestrictedArea():
    return render_template("RestrictedArea.html")

@app.route("/GuardRoom")
def GuardRoom():
    return render_template("GuardRoom.html")

@app.route("/Entrance")
def Entrance():
    return render_template("Entrance.html")
	
#===========================================================================================================================

#Entrance LED Related
@app.route("/readLED/")
def readPin():

	response = ledStatus()

	templateData = {
		'title' : 'Status of LED: ',
		'response' : response
	}

	return render_template('pin.html', **templateData)
   
#Entrance LED Related
@app.route("/writeLED1/<status>")
def writePin1(status):

	if status == 'On':
		response = led1On()
	else:
		response = led1Off()

	templateData = {
		'title' : 'Status of LED',
		'response' : response
	}

	return render_template('pin.html', **templateData)

#Entrance LED Related
@app.route("/writeLED2/<status>")
def writePin2(status):

	if status == 'On':
		response = led2On()
	else:
		response = led2Off()

	templateData = {
		'title' : 'Status of LED',
		'response' : response
	}
	
	return render_template('pin.html', **templateData)

#GuardRoom LED Related
@app.route("/writeLED3/<status>")
def writePin3(status):

	if status == 'On':
		response = led3On()
	else:
		response = led3Off()

	templateData = {
		'title' : 'Status of LED',
		'response' : response
	}

	return render_template('pin.html', **templateData)

#===========================================================================================================================	
app.run(debug=True,host="0.0.0.0")
