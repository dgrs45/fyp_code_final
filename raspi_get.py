import pyttsx3
import acapture
import cv2
import requests

engine = pyttsx3.init()   

try:

    cap = acapture.open(0) 
    while True:
        check,frame = cap.read() # non-blocking
        if check:
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            
            res = requests.post('http://192.168.29.9:5000/camera', data=frame.tolist())
            engine.say(res.json()['main_class_detected'])
            engine.runAndWait()
            cv2.waitKey(1)

except KeyboardInterrupt:
    pass