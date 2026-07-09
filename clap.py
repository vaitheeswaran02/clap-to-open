import sounddevice as sd
import numpy as np
import webbrowser

threshold = 0.5  # Adjust this threshold based on your microphone sensitivity
opened=False

def audio_callback(indata,frames,time,status):
    global opened

    volume= np.linalg.norm(indata) * 10

    if volume > threshold and not opened:
        print("clap detected")
        webbrowser.open("https://www.google.com")
        opened=True

print("listening for claps....")

with sd.InputStream(callback=audio_callback):
    while True:
        pass