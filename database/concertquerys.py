from database.database import Database
class ConcertQueries:
    def __init__(self, db_conn):
        self.db = db_conn

    def get_all_concert_ad(self):
       
        query = 'SELECT "etkinlikAd","img" FROM etkinlik;'
        users = self.db.execute_query(query, fetch=True)
        
     
        return users if users is not None else []
