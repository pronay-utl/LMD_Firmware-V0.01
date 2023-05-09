from gpiozero import LED,MotionSensor
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
from gpiozero import Buzzer
from time import sleep
import requests
import json
from picamera import PiCamera
from datetime import datetime
import os


#**************** Video finename and path ******************
# filename_part1="doorbell"
# file_ext=".mp4"
# now = datetime.now()
# current_datetime = now.strftime("%d-%m-%Y_%H:%M:%S")
# filename=filename_part1+"_"+current_datetime+file_ext
# filepath="/home/pi/doorbell/camera/"

# def remove_file():
#  if os.path.exists("/home/pi/doorbell/camera/newvideo.h264"):
#   os.remove("/home/pi/doorbell/camera/newvideo.h264")
#  else:
#   print("file does not exist")

#  if os.path.exists(filepath+filename):
#   os.remove(filepath+filename)
#  else:
#   print("file does not exist")

# def capture_video():
#  remove_file()
#  camera.start_preview()
#  camera.start_recording('/home/pi/doorbell/camera/newvideo.h264')

# def stop_video():
#  camera.stop_recording()
#  camera.stop_preview()
#  res=os.system("MP4Box -add /home/pi/doorbell/camera/newvideo.h264 /home/pi/doorbell/camera/newvideo.mp4")
#  os.system("mv /home/pi/doorbell/camera/newvideo.mp4 "+filepath+filename)

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

#***************** Initiate pi Camera **************************
# camera=PiCamera()
#***************** Program Start **************************
print("Device is now running !!")
while True:
    if pir.motion_detected:
    # start = input("Do you want to start :")
    # if start=="yes":
        print("Motion Detected")
        red.on
        # capture_video()
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
                # stop_video()

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
            # stop_video()
    sleep(2)