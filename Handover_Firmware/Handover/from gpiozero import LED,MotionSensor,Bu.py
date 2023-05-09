from gpiozero import LED,MotionSensor,Buzzer
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
from time import sleep
import requests
import json
from picamera import PiCamera
from datetime import datetime
import os


#**************** Sensors Initilize ******************
red = LED(18)
pir = MotionSensor(4)
buzzer = Buzzer(17)
pn532= Pn532_i2c()
pn532.SAMconfigure()
url = 'https://kni6zyml9b.execute-api.us-east-1.amazonaws.com/DEV/web/doorbell/unsigned/bell-to-bell-cloud'
#fake data
payload = {
    "tracking_id": "9",
    "order_id": "1004",
    "doorbell_id": "100001",
    "stream_url":"https://www.youtube.com/watch?v=P4gZP8YoWow"}
# Adding empty header as parameters are being sent in payload
headers = {
    "Content-Type":"application/json",
    "x-api-key":"caFG0mX4gjaLJGOWfTRLwVAyFPTqgt66uGfgtDd3"
}
#***************** Program Start **************************
print("Device is now running !!")
while True:
    if pir.motion_detected:
        print("Motion Detected")
        red.on
        print("Please choose a option below !")
        print("Option 1 Tap your NFC enabled device")
        print("Option 2 Manual entry")
        option = input("Please Choose an option to continue : ")
        if option=="1":
            buzzer.on()
            print("Please tap your device to continue !")
            card_data = pn532.read_mifare().get_data()
            if card_data :
                sleep(1)
                buzzer.off()
                r = requests.post(url, data=json.dumps(payload), headers=headers)
                print(r.json().get('message'))
                red.off

        else :
            tracking_id = input("Enter tracking id : ")
            order_id = input("Enter order id : ")
            doorbell_id = input("Enter doorbell id : ")
            stream_url = input("Enter video streaming url : ")
            payload = {
                "tracking_id": tracking_id,
                "order_id": order_id,
                "doorbell_id": doorbell_id,
                "stream_url":stream_url}
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            print(r.json().get('message'))
            red.off
    sleep(2)