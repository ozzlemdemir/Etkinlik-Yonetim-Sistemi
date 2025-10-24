from flask import Flask
from app.app_routes import app_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = "çok_gizli_bir_anahtar"

    # Blueprint kaydı
    app.register_blueprint(app_routes)

    return app