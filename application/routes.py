import os
import secrets
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
from flask import Blueprint, render_template, request, g ,redirect, url_for
from application.forms import QRcodeForm

blp = Blueprint("routes", __name__, static_folder="static", template_folder="templates")

base_dir = os.path.abspath(os.path.dirname(__file__))
static_folder = os.path.join(base_dir, "static")

decoded_info = []

@blp.route("/")
def index():
    return render_template("index.html")

@blp.route("/generate", methods=["POST","GET"])
def generate():
    form = QRcodeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            data = form.convert.data
            image_name = f"{secrets.token_hex(10)}.png"
            qrcode_loc = f"{static_folder}/{image_name}"
            try:
                qr = qrcode.QRCode(version=10,
                                   error_correction=qrcode.constants.ERROR_CORRECT_M,
                                   box_size=10,
                                   border=5)
                qr.make(fit=True)
                qr.add_data(data)
                img = qr.make_image(fill_color='blue',
                                    back_color='white')
                img.save(f"{qrcode_loc}")
            except Exception as e:
                print(str(e))

            return render_template("generated_code.html", title="Magic has happened", image=image_name)
    return render_template("generate_code.html", title="Welcome to the magic page!!", form=form)

@blp.route("/upload", methods=["POST","GET"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        filename, extension = file.filename.split(".")
        generated_filename = secrets.token_hex(20) + f".{extension}"

        file_loc = os.path.join(static_folder, generated_filename)
        file.save(file_loc)

        decodeQR = decode(Image.open(file_loc))

        info = decodeQR[0].data.decode("ascii")

        decoded_info.append(info)

        print(decoded_info)
        os.remove(file_loc)

    return render_template("upload.html", title="Scan the qr code here")

@blp.route("/decoded")
def decoded():

    return render_template("decoded.html", title="Decoded", info=decoded_info)
