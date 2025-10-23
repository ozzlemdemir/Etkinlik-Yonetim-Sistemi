from app.database.database import Database
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
