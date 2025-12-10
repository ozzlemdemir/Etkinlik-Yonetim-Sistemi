from flask import Flask, request, session
from itsdangerous import URLSafeTimedSerializer, BadSignature
from app.app_routes import app_routes

serializer = URLSafeTimedSerializer("SECRET_KEY")

def create_app():
    app = Flask(__name__)
    app.secret_key = "çok_gizli_bir_anahtar"

    app.register_blueprint(app_routes)

    @app.before_request
    def auto_login():
        if "user_id" not in session:
            token = request.cookies.get("remember_token")

            if token:
                try:
                    user_id = serializer.loads(token, max_age=60*60*24*7)
                    

                    from app.services.user_service import UserService
                    user = UserService().get_user_by_id_for_remember_token(user_id)

                    if user and user[5] == token:  # remember_token eşleşiyor mu
                        session["user_id"] = user[0]
                        session["user_name"] = user[1]
                        session["role"] = user[4]
                        print("AUTO LOGIN USER:", user)
                        print("ROLE FROM USER:", user[4])

                        session["remember_login"]=True
                        session["after_remember_login"] = "admin_dashboard" if user[4] == "admin" else "index"

                except Exception:
                    pass
    return app
