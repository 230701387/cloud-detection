from flask import Flask, render_template, request
from model import predict_image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    confidence = None
    filename = None

    if request.method == "POST":

        file = request.files.get("file")

        if not file or file.filename == "":
            return render_template("index.html", result="No file selected")

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        try:
            file.save(filepath)

            result, confidence = predict_image(filepath)

        except Exception as e:
            result = f"Error: {str(e)}"
            confidence = None

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        filename=filename
    )


# Azure doesn't use this, but keep it safe
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)