from app.database.database import Database
import bcrypt
class UserQueries:

    def __init__(self, db_conn):
        self.db = db_conn

    def get_all_users(self):
       
        query = 'SELECT userID, name, mail FROM users;'
        try:
            users = self.db.execute_query(query, fetch=True)
            return users if users is not None else []
        except Exception as e:
            print("Sorgu hatası:", e)
            self.db.conn.rollback()  
            return []

    def get_user_by_email_and_password(self, email, password):
        query = "SELECT * FROM users WHERE mail = %s AND password = %s ;"
        try:
            result = self.db.execute_query(query, (email, password), fetch=True)
            return result[0] if result else None
        except Exception as e:
            print("Giriş sorgusu hatası:", e)
            return None
    
    def get_user_by_id(self, user_id):
        query = "SELECT userID, name FROM users WHERE userID = %s;"
        try:
            user = self.db.execute_query(query, (user_id,), fetch=True)
            return user[0] if user else None
        except Exception as e:
            print("Kullanıcı çekme hatası:", e)
            return None
    
    def create_user(self, name, email, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        query = 'INSERT INTO users (name, mail, password, "roleID") VALUES (%s, %s, %s, %s);'
        try:
            self.db.execute_query(query, (name, email, hashed_password.decode('utf-8'), 100))#100 kullanıcı rolu id
            return True
        except Exception as e:
            print("Kullanıcı oluşturma hatası:", e)
            self.db.conn.rollback()
            return False

    
    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE mail = %s;"
        try:
            result = self.db.execute_query(query, (email,), fetch=True)
            return result[0] if result else None
        except Exception as e:
            print("E-posta ile kullanıcı çekme hatası:", e)
            return None
    
    def bildirimleri_getir(self, kullanici_id):
        query = "SELECT mesaj, tarih FROM bildirimler WHERE alici_id = %s ORDER BY tarih DESC;"
        try:
            result = self.db.execute_query(query, (kullanici_id,), fetch=True)
            if not result:
                return []  # eğer None ya da boşsa boş liste döndür
            return [{"mesaj": r[0], "tarih": r[1]} for r in result]
        except Exception as e:
            print("Bildirim sorgu hatası:", e)
            return []
        
   
        
    def token_kaydetme(self, user_id, token):
        query = "UPDATE users SET remember_token = %s WHERE userID = %s;"
        try:
            self.db.execute_query(query, (token, user_id))
            self.db.conn.commit()
        except Exception as e:
            print("Token kaydetme hatası:", e)
            self.db.conn.rollback()

    def get_user_by_id_for_remember_token(self, user_id):
        query = """
            SELECT 
                userid,
                name,
                mail,
                password,
                "roleID",
                remember_token
            FROM users
            WHERE userid = %s;
        """
        try:
            user = self.db.execute_query(query, (user_id,), fetch=True)
            return user[0] if user else None
        except Exception as e:
            print("Kullanıcı çekme hatası:", e)
            self.db.conn.rollback()
            return None
            
            
    def get_admin_by_id(self, admin_id):
        query = 'SELECT userid, name, mail, password FROM users WHERE "roleID" = 101 AND userid = %s;'
        results = self.db.execute_query(query, (admin_id,), fetch=True)
        
        if results:
            user_tuple = results[0]
  
            admin_data = {
                'userid': user_tuple[0],
                'name': user_tuple[1], 
                'mail': user_tuple[2], 
                'password': user_tuple[3]
            }
            return admin_data
        else:
            return None
        
    def admin_isim_guncelle(self,admin_id,new_name):
        query='UPDATE users SET name=%s WHERE userid=%s AND "roleID" = 101;'
        try:
            self.db.execute_query(query,(new_name,admin_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print("Admin isim güncelleme hatası:", e)
            self.db.conn.rollback()
            return False
        
    def admin_mail_guncelle(self,admin_id,new_mail):
        query='UPDATE users SET mail=%s WHERE userid=%s AND "roleID" = 101;'
        try:
            self.db.execute_query(query,(new_mail,admin_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print("Admin mail güncelleme hatası:", e)
            self.db.conn.rollback()
            return False
        
    def admin_sifre_guncelle(self, admin_id, new_hashed_password_str):
    
        query = 'UPDATE users SET password = %s WHERE userid = %s AND "roleID" = 101;'
        try:
            self.db.execute_query(query, (new_hashed_password_str, admin_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print("Admin şifre güncelleme hatası:", e)
            self.db.conn.rollback()
            return False
      
      
    def get_user_by_id_profil(self, user_id):
        query = 'SELECT userid, name, mail, password FROM users WHERE "roleID" = 100 AND userid = %s;'
        results = self.db.execute_query(query, (user_id,), fetch=True)
        
        if results:
            user_tuple = results[0]
  
            user_data = {
                'userid': user_tuple[0],
                'name': user_tuple[1], 
                'mail': user_tuple[2], 
                'password': user_tuple[3]
            }
            return user_data
        else:
            return None  
    def user_isim_guncelle(self,user_id,new_name):
        query='UPDATE users SET name=%s WHERE userid=%s AND "roleID" = 100;'
        try:
            self.db.execute_query(query,(new_name,user_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print("Kullanıcı isim güncelleme hatası:", e)
            self.db.conn.rollback()
            return False
    def user_mail_guncelle(self,user_id,new_mail):
        query='UPDATE users SET mail=%s WHERE userid=%s AND "roleID" = 100;'
        try:
            self.db.execute_query(query,(new_mail,user_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print("Kullanıcı mail güncelleme hatası:", e)
            self.db.conn.rollback()
            return False
    def user_sifre_guncelle(self, user_id, new_hashed_password_str):
    
        query = 'UPDATE users SET password = %s WHERE userid = %s AND "roleID" = 100;'
        try:
            self.db.execute_query(query, (new_hashed_password_str, user_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print("Kullanıcı şifre güncelleme hatası:", e)
            self.db.conn.rollback()
            return False
        
        
#şifremi unuttum ile ilgili fonksiyonlar
    def find_user_by_mail(self, email):
        query = "SELECT userid, name, mail FROM users WHERE mail = %s;"
        try:
            result = self.db.execute_query(query, (email,), fetch=True)
            return result[0] if result else None
        except Exception as e:
            print("E-posta ile kullanıcı arama hatası:", e)
            return None

    def insert_reset_token(self, user_id, token, expiration):
        query = '''INSERT INTO password_resets (user_id, token, expiration) 
                  VALUES (%s, %s, %s);'''
        try:
            self.db.execute_query(query, (user_id, token, expiration))
            self.db.conn.commit()
            return True
        except Exception as e:
            print("Reset token ekleme hatası:", e)
            self.db.conn.rollback()
            return False
    
    def token_gecerli_mi(self,token):
        query = '''SELECT user_id FROM password_resets 
                   WHERE token = %s AND expiration > NOW();'''
        try:
            result = self.db.execute_query(query, (token,), fetch=True)
            return result[0][0] if result else None
        except Exception as e:
            print("Token geçerlilik kontrol hatası:", e)
            return None
    def token_kullanildi(self,token):
        query = '''UPDATE password_resets SET is_used = TRUE WHERE token = %s;'''
        try:
            self.db.execute_query(query, (token,))
            self.db.conn.commit()
            return True
        except Exception as e:
            print("Token kullanım güncelleme hatası:", e)
            self.db.conn.rollback()
            return False
    def update_user_password_by_id(self, user_id, hashed_password):
       
        query = 'UPDATE users SET password = %s WHERE userid = %s;'
        try:
            self.db.execute_query(query, (hashed_password, user_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print("Şifre güncelleme hatası:", e)
            self.db.conn.rollback()
            return False
        
#admin dashboard istatistik fonksiyonları
    def toplam_kullanici_sayisi(self):
        query = 'SELECT COUNT(*) FROM users WHERE "roleID" = 100;'
        try:
            result = self.db.execute_query(query, fetch=True)
            return result[0][0] if result else 0
        except Exception as e:
            print("Toplam kullanıcı sayısı sorgu hatası:", e)
            return 0
    def toplam_etkinlik_sayisi(self):
        query = 'SELECT COUNT(*) FROM etkinlik;'
        try:
            result = self.db.execute_query(query, fetch=True)
            return result[0][0] if result else 0
        except Exception as e:
            print("Toplam etkinlik sayısı sorgu hatası:", e)
            return 0
    def aktif_etkinlik_sayisi(self):
        query = 'SELECT COUNT(*) FROM etkinlik WHERE tarih >= NOW();'
        try:
            result = self.db.execute_query(query, fetch=True)
            return result[0][0] if result else 0
        except Exception as e:
            print("Aktif etkinlik sayısı sorgu hatası:", e)
            return 0
    def satilan_bilet_sayisi(self):
        query = 'SELECT COUNT(*) FROM biletler;'
        try:
            result = self.db.execute_query(query, fetch=True)
            return result[0][0] if result else 0
        except Exception as e:
            print("Satılan bilet sayısı sorgu hatası:", e)
            return 0
    def get_all_kategoriler(self):
        query = 'SELECT kategoriid, kategori_adi FROM kategori;'
        try:
            kategoriler = self.db.execute_query(query, fetch=True)
            return kategoriler if kategoriler is not None else []
        except Exception as e:
            print("Kategoriler sorgu hatası:", e)
            self.db.conn.rollback()  
            return []