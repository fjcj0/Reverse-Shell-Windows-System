from flask import Flask,request
import os
from datetime import datetime
app = Flask(__name__)
upload_folder = "screenshots"
os.makedirs(upload_folder,exist_ok=True)
@app.route('/upload-picture',methods=["POST"])
def upload_picture():
    if "image" not in request.files:
        return "No Images",400
    image = request.files["image"]
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
    path = os.path.join(upload_folder,filename)
    image.save(path)
    return "OK", 200
@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    if "audio" not in request.files:
        return "No audio", 400
    audio = request.files["audio"]
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"
    path = os.path.join("audio", filename)
    os.makedirs("audio", exist_ok=True)
    audio.save(path)
    return "OK", 200
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=2020)