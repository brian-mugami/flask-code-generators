import os.path
from flask import Flask
import secrets
from flask_dropzone import Dropzone

base_dir = os.path.abspath(os.path.dirname(__file__))
dropzone = Dropzone()

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_urlsafe(nbytes=16)
    dropzone.init_app(app)
    app.config["DROPZONE_REDIRECT_VIEW"] = "routes.decoded"
    from .routes import blp as routeblueprint

    app.register_blueprint(routeblueprint)

    return app