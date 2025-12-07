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
            