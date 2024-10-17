import pyaudio
import numpy as np

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)

def generate_tone(frequency, duration=1, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)  
    return tone

height = float(input("Please enter your height (cm):"))
age = float(input("Please enter your age:"))

frequency = height * age

height_tone = generate_tone(frequency)
stream.write(height_tone.astype(np.float32).tobytes())
print("Audio is playing at the frequency: {:.1f} Hz".format(frequency))
    

