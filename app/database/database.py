import psycopg2

class Database:
    _instance = None  # Singleton 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self, host="localhost", database="EtkinlikApp", user="postgres", password="samsun55"):
        if not hasattr(self, 'conn'):  # sadece ilk seferde bağlantı kur
            self.host = host
            self.database = database
            self.user = user
            self.password = password
            self.conn = None

    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
                print("Veritabanı bağlantısı başarılı!")
            except Exception as e:
                print("Veritabanı bağlantı hatası:", e)
        return self.conn
            
            
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
