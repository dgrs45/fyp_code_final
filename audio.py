import math
import numpy as np
import sounddevice as sd

sample_rate = 44100
duration = 1.0
volume = 0.5

def generate_audio(distance_cm, channel):
    # Calculate frequency and amplitude based on distance
    frequency = 220 - (distance_cm / 10)  # Adjust the scaling as needed
    amplitude = 0.5 + (distance_cm / 2000)  # Adjust the scaling as needed

    amplitude = max(0, min(1, amplitude))

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = (amplitude * 32767.0 * np.sin(2 * np.pi * frequency * t)).astype(np.int16)
    
    return signal

try:
    while True:
        distance_cm = float(input("Enter distance (in centimeters): "))
        if distance_cm <= 0:
            break
        channel = np.random.randint(1,3)
        audio_signal = generate_audio(distance_cm, channel)
        sd.play(audio_signal, sample_rate, mapping=[channel])
        sd.wait()

except KeyboardInterrupt:
    print('BAIGAN')

