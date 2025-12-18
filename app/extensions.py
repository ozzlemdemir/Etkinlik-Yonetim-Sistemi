# app/extensions.py
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

mail = Mail()
serializer = URLSafeTimedSerializer("SECRET_KEY") # Buraya taşıdık