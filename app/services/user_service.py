# app/services/user_service.py
import bcrypt
from app.database.userquerys import UserQueries
from app.database.database import Database

class UserService:
    def __init__(self):
        self.db = Database()  
        self.db.connect()     
        self.query = UserQueries(self.db)

    def login(self, email, password):
        user = self.query.get_user_by_email(email)
        if user:
            stored_hash = user[3].encode('utf-8')  # 3. sütun password olmalı
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                return {"success": True, "user": user}
        return {"success": False, "message": "E-posta veya şifre hatalı!"}
        
    def indexte_user_by_id(self, user_id):
        return self.query.get_user_by_id(user_id)

    def register(self, name, email, password):
        existing_user = self.query.get_user_by_email(email)
        if existing_user:
            return {"success": False, "message": "Bu e-posta zaten kayıtlı!"}
        
        created = self.query.create_user(name, email, password)
        if created:
            return {"success": True}
        else:
            return {"success": False, "message": "Kayıt sırasında bir hata oluştu."}