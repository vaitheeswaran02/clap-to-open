import sounddevice as sd
import numpy as np
import webbrowser
import subprocess
import time

# ---------------- SETTINGS ---------------- #

THRESHOLD = 0.25      # Adjust according to your microphone
WINDOW_TIME = 2       # Wait for next clap
COOLDOWN = 0.5        # Ignore duplicate clap

# ------------------------------------------ #

clap_count = 0
last_clap_time = 0


def launch_app(count):

    if count == 1:
        print("\n🌐 Opening Google...")
        webbrowser.open("https://www.google.com")

    elif count == 2:
        print("\n▶ Opening YouTube...")
        webbrowser.open("https://www.youtube.com")

    elif count == 3:
        print("\n🐙 Opening GitHub...")
        webbrowser.open("https://github.com")

    elif count == 4:
        print("\n💻 Opening VS Code...")
        try:
            subprocess.Popen("code")
        except:
            print("VS Code not found!")

    else:
        print(f"\n{count} claps detected. No action assigned.")


def audio_callback(indata, frames, time_info, status):

    global clap_count
    global last_clap_time

    peak = np.max(np.abs(indata))

    current = time.time()

    # Detect only if enough time has passed since previous clap
    if peak > THRESHOLD and (current - last_clap_time) > COOLDOWN:

        clap_count += 1
        last_clap_time = current

        print(f"👏 {clap_count} Clap Detected")


print("=" * 40)
print("🎤 Listening for claps...")
print("=" * 40)

stream = sd.InputStream(
    channels=1,
    samplerate=44100,
    blocksize=2048,
    callback=audio_callback
)

stream.start()

try:

    while True:

        time.sleep(0.1)

        if clap_count > 0:

            # Wait to see if more claps come
            if time.time() - last_clap_time > WINDOW_TIME:

                launch_app(clap_count)

                clap_count = 0

except KeyboardInterrupt:

    print("\nStopped!")

finally:

    stream.stop()
    stream.close()
