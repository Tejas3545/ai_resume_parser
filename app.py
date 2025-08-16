from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
from resume_parser import extract_text, parse_resume
from database import save_to_db, get_all_resumes, delete_resume

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

app = Flask(__name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "docx"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    # Renders templates/index.html
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return redirect(url_for("home"))

    file = request.files["resume"]
    if not file or file.filename.strip() == "":
        return redirect(url_for("home"))

    if not allowed_file(file.filename):
        # Just bounce back silently; you can replace with flash if you add a secret_key.
        return redirect(url_for("home"))

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Parse resume
    text = extract_text(filepath)
    data = parse_resume(text)  # dict with name, email, phone, skills, education, experience
    save_to_db(data)

    return render_template("result.html", data=data)


@app.route("/resumes", methods=["GET"])
def resumes_page():
    data = get_all_resumes()
    return render_template("resumes.html", resumes=data)


@app.route("/api/resumes", methods=["GET"])
def get_resumes():
    data = get_all_resumes()
    return jsonify(data)


@app.route("/delete/<int:resume_id>", methods=["DELETE"])
def delete_resume_api(resume_id: int):
    delete_resume(resume_id)
    return jsonify({"message": f"Resume with ID {resume_id} deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
