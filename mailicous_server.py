from flask import Flask, request, jsonify
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import json
app = Flask(__name__)
LOG_FILE = os.path.join(os.path.dirname(__file__), "locations.log")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
def log_to_file(data):
    timestamp = datetime.utcnow().isoformat()
    line = f"[{timestamp}] {json.dumps(data)}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
@app.route("/upload", methods=["POST"])
def upload_files():
    if "files" not in request.files:
        return jsonify({"error": "There are no files"}), 400
    files = request.files.getlist("files")
    saved_files = []
    for file in files:
        if file.filename == "":
            continue
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        try:
            file.save(file_path)
            saved_files.append({
                "filename": filename,
                "path": file_path
            })
        except Exception as e:
            return jsonify({"error": f"Failed save file: {file.filename}: {str(e)}"}), 500
    if not saved_files:
        return jsonify({"error": "The file didn't save"}), 400
    return jsonify({
        "message": "Folder has been uploaded",
        "files": saved_files
    }), 200
@app.route("/get-location", methods=["POST"])
def get_location():
    location = request.get_json()
    if not location:
        return jsonify({"status": "error", "message": "No JSON received"}), 400
    print("📍 Location received:", location)
    log_to_file(location)
    return jsonify({"status": "ok", "saved": True})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2020, debug=True, threaded=True)