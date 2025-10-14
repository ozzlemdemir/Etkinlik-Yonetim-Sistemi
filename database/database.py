import psycopg2

class Database:
    def __init__(self, host="localhost", database="EtkinlikApp", user="postgres", password="1234"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print(" Veritabanına bağlanıldı.")
        except Exception as e:
            print("Veritabanı bağlantı hatası:", e)
            
            
    def execute_query(self, query, params=None, fetch=False):
        if self.conn is None:
            print("Veritabanı bağlantısı kurulmamış.")
            return None 
            
        try:
            cur = self.conn.cursor() 
            cur.execute(query, params)
            
            if fetch:
                data = cur.fetchall()
                cur.close()
                return data
            else:
                self.conn.commit()
                cur.close()
                
        except Exception as e:
            print("Sorgu hatası:", e)
            return None # Hata durumunda None döndür
