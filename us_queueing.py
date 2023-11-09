import RPi.GPIO as GPIO
import time
import threading
import sounddevice as sd
from queue import Queue

from audio_fins import generate_audio


sample_rate = 44100
# Set the GPIO mode
GPIO.setmode(GPIO.BOARD)

# Define the GPIO pins
us1_trig = 12
us1_echo = 16

us2_trig = 22
us2_echo = 24

us3_trig = 11
us3_echo = 13

# Set the pins as input or output
GPIO.setup(us1_trig, GPIO.OUT)
GPIO.setup(us1_echo, GPIO.IN)


GPIO.setup(us2_trig, GPIO.OUT)
GPIO.setup(us2_echo, GPIO.IN)


GPIO.setup(us3_trig, GPIO.OUT)
GPIO.setup(us3_echo, GPIO.IN)



def f1(q1):
    while True:
        GPIO.output(us1_trig, False)
        time.sleep(0.2)
        GPIO.output(us1_trig, True)
        time.sleep(0.2)
        GPIO.output(us1_trig, False)

        while GPIO.input(us1_echo) == 0:
            us1_pulse_start = time.time()
        while GPIO.input(us1_echo) == 1:
            us1_pulse_end = time.time()

        us1_pulse_duration = us1_pulse_end - us1_pulse_start
        us1_distance = us1_pulse_duration * 17150  # Speed of sound in cm/s
        q1.put(us1_distance)




def f2(q2):
    while True:
        GPIO.output(us2_trig, False)
        time.sleep(0.2)
        GPIO.output(us2_trig, True)
        time.sleep(0.2)
        GPIO.output(us2_trig, False)
        while GPIO.input(us2_echo) == 0:
            us2_pulse_start = time.time()
        while GPIO.input(us2_echo) == 1:
            us2_pulse_end = time.time()

        us2_pulse_duration = us2_pulse_end - us2_pulse_start
        us2_distance = us2_pulse_duration * 17150
        q2.put(us2_distance)


def f3(q):
    while True:
        GPIO.output(us3_trig, False)
        time.sleep(0.2)
        GPIO.output(us3_trig, True)
        time.sleep(0.2)
        GPIO.output(us3_trig, False)
        while GPIO.input(us3_echo) == 0:
            us3_pulse_start = time.time()
        while GPIO.input(us3_echo) == 1:
            us3_pulse_end = time.time()

        us3_pulse_duration = us3_pulse_end - us3_pulse_start
        us3_distance = us3_pulse_duration * 17150
        q3.put(us3_distance)

def f4(q):
    while True:
        data1 = q1.get()
        data2 = q2.get()
        data3 = q3.get()
        dist = [data1, data2, data3]
        min_dist = min(dist)
        if min_dist<500:
            audio_signal = generate_audio(min_dist,dist.index(min_dist))
            sd.play(audio_signal, sample_rate, mapping=[dist.index(min_dist)])
            sd.wait()
        print('in queueing func')
        q1.task_done()
        q2.task_done()
        q3.task_done()    


q1 = Queue()
q2 = Queue()
q3 = Queue()
thread1 = threading.Thread(target=f1, args=(q1, ))
thread2 = threading.Thread(target=f2, args=(q2, ))
thread3 = threading.Thread(target=f3, args=(q3, ))

try:
    thread1.start()
    thread2.start()
    thread3.start()


except KeyboardInterrupt:
    thread1.join()
    thread2.join()
    thread3.join()
