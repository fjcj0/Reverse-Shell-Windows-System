const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const morgan = require('morgan');
const app = express();
const PORT = 2020;
const UPLOAD_FOLDER = path.join(__dirname, "uploads");
const LOG_FILE = path.join(__dirname, "locations.log");
app.use(morgan('dev'));
app.use(express.json());  
app.use(express.text());      
function logToFile(data) {
    const timestamp = new Date().toISOString();
    const line = `[${timestamp}] ${JSON.stringify(data)}\n`;
    fs.appendFileSync(LOG_FILE, line, "utf8");
}
if (!fs.existsSync(UPLOAD_FOLDER)) {
  fs.mkdirSync(UPLOAD_FOLDER);
}
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, UPLOAD_FOLDER);
  },
  filename: function (req, file, cb) {
    const timestamp = new Date().toISOString().replace(/[-:.TZ]/g, "_");
    const safeName = file.originalname.replace(/\s+/g, "_");
    cb(null, `${timestamp}_${safeName}`);
  },
});
const upload = multer({ storage: storage });
app.post("/upload", upload.array("files"), (req, res) => {
  if (!req.files || req.files.length === 0) {
    return res.status(400).json({ error: "There are no files" });
  }
  const savedFiles = req.files.map((file) => ({
    filename: file.filename,
    path: file.path,
  }));
  res.status(200).json({
    message: "Files have been uploaded",
    files: savedFiles,
  });
});
app.post("/get-location", (req, res) => {
    let location = req.body;
    if (typeof location === "string") {
        location = { raw: location };
    }
    if (!location) {
        return res.status(400).json({ status: "error", message: "No data received" });
    }
    logToFile(location);
    res.json({ status: "ok", saved: true });
});
app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running on http://0.0.0.0:${PORT}`);
});