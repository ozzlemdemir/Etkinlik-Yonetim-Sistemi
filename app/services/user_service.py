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
            stored_hash = user[3].encode('utf-8')  # password sütunu
            role = user[4]  # roleID sütunu

            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                if role == 100:
                    return {"success": True, "user": user, "role": "user"}
                elif role == 101:
                    return {"success": True, "user": user, "role": "admin"}
                else:
                    return {"success": False, "message": "Geçersiz rol!"}

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
        
    def bildirimleri_getir(self, kullanici_id):
        return self.query.bildirimleri_getir(kullanici_id)
    
    def get_user_by_id_for_remember_token(self, user_id):
        return self.query.get_user_by_id_for_remember_token(user_id)

    def kaydet_remember_token(self, user_id, token):
        return self.query.token_kaydetme(user_id, token)
    
    #admin servis fonksiyonları(profil bilgileri için)
    def get_admin_by_id(self, user_id):
        return self.query.get_admin_by_id(user_id)
    def admin_isim_guncelleme(self, user_id, yeni_isim):
        return self.query.admin_isim_guncelle(user_id, yeni_isim)
    def admin_mail_guncelleme(self, user_id, yeni_mail):
        return self.query.admin_mail_guncelle(user_id, yeni_mail)
    def admin_sifre_guncelleme(self, user_id, yeni_sifre):
        return self.query.admin_sifre_guncelle(user_id, yeni_sifre)
    
    #"user" servis fonksiyonları(profil bilgileri için)
    def get_user_by_id_profil(self, user_id):
        return self.query.get_user_by_id_profil(user_id)
    def user_isim_guncelleme(self, user_id, yeni_isim):
        return self.query.user_isim_guncelle(user_id, yeni_isim)
    def user_mail_guncelleme(self, user_id, yeni_mail):
        return self.query.user_mail_guncelle(user_id, yeni_mail)
    def user_sifre_guncelleme(self, user_id, yeni_sifre):
        return self.query.user_sifre_guncelle(user_id, yeni_sifre)

    
       