# Tested in Python 3.5.3
import datetime  # Importing the datetime library
import telepot   # Importing the telepot library
from telepot.loop import MessageLoop    # Library function to communicate with telegram bot
from time import sleep      # Importing the time library to provide the delays in program
import json
import urllib.request
import requests
import base64
import time
import os
# Settings for the domoticz server

domoticzserver   = "127.0.0.1:8080"
domoticzusername = ""
domoticzpassword = ""



# Create virtual sensors in dummy hardware

# Sensor IDs
idx_act_tkm="44"
idx_act_fuel="45"
idx_act_tcost="46"
idx_act_km="47"
idx_act_consumption="48"
idx_act_cost="49"


base64string = base64.encodestring(('%s:%s' % (domoticzusername, domoticzpassword)).encode()).decode().replace('\n', '')


def domoticzrequest (url):
  print(url)
  request = urllib.request.Request(url)
  request.add_header("Authorization", "Basic %s" % base64string)
  response = urllib.request.urlopen(request)
  return response.read()

def domoticzread(idx,RData):
    url = "http://" + domoticzserver + "/json.htm?type=devices&rid=" + idx
    response = requests.get(url)
    jsonData = json.loads(response.text)
    #print(jsonData)
    result = jsonData["result"][0][RData]
    return result;

def domoticzrequest (url):
    #print(url)
    request = urllib.request.Request(url)
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib.request.urlopen(request)
    return response.read()

def domoticzread2(idx,RData):
    url = "http://" + domoticzserver + "/json.htm?type=devices&rid=" + idx
    response = requests.get(url)
    jsonData = json.loads(response.text)
    #print(jsonData)
    result = jsonData["result"][0][RData]
    result2=result.split(" ",1)
    return result2[0];

def domoticzwrite(idx,WData):
    domoticzrequest("http://" + domoticzserver + "/json.htm?type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue=" + WData)
    
def calculation_fuel(act_tkm,act_fuel,act_tcost):
    err=""
    last_km=domoticzread2(idx_act_tkm,"Data")
    try:
      act_km=round(float(act_tkm)-float(last_km),2)
    except: err = err+"act_km err;"
    try:
      act_consumption=round((float(act_fuel)/act_km)*100,2)
    except: err = err+"act_consuption err;"
    try:
      act_cost=round(float(act_tcost)/act_km,2)
    except: err =err+"act_cost err;"  
    if err =="":
      domoticzwrite(idx_act_tkm,str(act_tkm))
      domoticzwrite(idx_act_fuel,str(act_fuel))
      domoticzwrite(idx_act_tcost,str(act_tcost))
      domoticzwrite(idx_act_km,str(act_km))
      domoticzwrite(idx_act_consumption,str(act_consumption))
      domoticzwrite(idx_act_cost,str(act_cost))
      result=str(act_km) + " km;" + str(act_consumption) + " l/100km;" + str(act_cost) + " Ft/km"
      return result
    else: return err

now = datetime.datetime.now() # Getting date and time




def handle(msg):
    chat_id = msg['chat']['id'] # Receiving the message from telegram
    command = msg['text']   # Getting text from the message
    command2 = command.split(";")
    command3 = command2[0]
    err = ""
    
    print ('Received:')
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == '/hi':
        bot.sendMessage (chat_id, str("Hi! Gabor"))
        
    elif command == '/time':
        bot.sendMessage(chat_id, str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second))
    elif command == '/date':
        bot.sendMessage(chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
    
    elif command3 == '/km':
        try:
          act_tkm = command2[1]
        except: err = err + "Error 1;"
        try:
          act_fuel = command2[2]
        except: err = err + "Error2 2;" 
        try:
          act_tcost = command2[3]
        except: err = err + "Error 3"
        if err =="":
          answer=calculation_fuel(act_tkm,act_fuel,act_tcost)
          bot.sendMessage(chat_id, answer)
        else:
          bot.sendMessage(chat_id, err)
        
        #GPIO.output(green_led_pin, False)

# Insert your telegram token below
bot = telepot.Bot('..............')
print (bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print ('Listening....')

while 1:
    sleep(10)
