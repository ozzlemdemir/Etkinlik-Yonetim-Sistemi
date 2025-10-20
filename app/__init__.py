from flask import Flask
from app.app_routes import app_routes

def create_app():
    app = Flask(__name__)

    # Blueprint kaydı
    app.register_blueprint(app_routes)

    return app