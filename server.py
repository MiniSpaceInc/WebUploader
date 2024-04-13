import os

from flask import Flask, jsonify, redirect, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.getcwd(), "blob")
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post("/upload/<uuid:event_uuid>")
def upload_file(event_uuid):
    if "file" not in request.files:
        return jsonify({"message": "No selected part"}), 400
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        mkdir(app.config["UPLOAD_FOLDER"], str(event_uuid))
        path = os.path.join(app.config["UPLOAD_FOLDER"], str(event_uuid), filename)
        file.save(path)
        return (
            jsonify({"message": "File uploaded successfully", "filename": filename}),
            200,
        )
    return (jsonify({"message": "Upload failed"}), 400)


@app.get("/images/<uuid:event_uuid>/<filename>")
def download_file(event_uuid, filename):
    path = os.path.join(app.config["UPLOAD_FOLDER"], str(event_uuid))
    return send_from_directory(path, filename)


def mkdir(parent_dir: str, dir: str) -> None:
    try:
        path = os.path.join(parent_dir, dir)
        os.mkdir(path)
    except FileExistsError:
        pass


@app.route("/")
def index():
    return """<img src="http://localhost:5000/images/9f9a74b3-6705-487e-bdc6-0c23a8728c14/TCS-roster.png" alt="W3Schools.com">"""
