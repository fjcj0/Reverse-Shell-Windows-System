from flask import Flask, request, jsonify
import os
from datetime import datetime
from werkzeug.utils import secure_filename
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
@app.route("/upload", methods=["POST"])
def upload_files():
    if "files" not in request.files:
        return jsonify({"error": "there are no files"}), 400
    files = request.files.getlist("files")
    saved_files = []
    for file in files:
        if file.filename == "":
            continue
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        saved_files.append({
            "filename": filename,
            "path": file_path
        })
    if not saved_files:
        return jsonify({"error": "No files to save"}), 400
    return jsonify({
        "message": "Files Have Been Uploaded",
        "files": saved_files
    }), 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2020, debug=True)