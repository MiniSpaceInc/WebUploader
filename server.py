import os
import shutil

from flask import Flask, jsonify, redirect, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.getcwd(), "blob")
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def mkdir(parent_dir: str, dir: str) -> None:
    try:
        path = os.path.join(parent_dir, dir)
        os.mkdir(path)
    except FileExistsError:
        pass


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


@app.delete("/images/<uuid:event_uuid>/<filename>")
def delete_file(event_uuid, filename):
    path = os.path.join(app.config["UPLOAD_FOLDER"], str(event_uuid), filename)
    os.remove(path)
    return (
        jsonify({"message": "File deleted successfully", "filename": filename}),
        200,
    )


@app.delete("/images/<uuid:event_uuid>")
def delete_all_files(event_uuid):
    path = os.path.join(app.config["UPLOAD_FOLDER"], str(event_uuid))
    shutil.rmtree(path)
    return (
        jsonify({"message": "Event deleted successfully", "event_uuid": event_uuid}),
        200,
    )
