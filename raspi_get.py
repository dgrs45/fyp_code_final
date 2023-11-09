import pyttsx3
import acapture
import torch
import cv2

model = torch.hub.load('ultralytics/yolov5', 'yolov5s') 
engine = pyttsx3.init()   
engine.runAndWait()
import requests
try:
    while True:
        res = requests.get('http://192.168.29.9:5000/camera')
        print(res.json())
        engine.say(res.json()['main_class_detected'])
        engine.runAndWait()
except KeyboardInterrupt:
    pass