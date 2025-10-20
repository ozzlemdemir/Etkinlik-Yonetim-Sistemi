from app.database.concertquerys import ConcertQueries
from app.database.database import Database

class ConcertService:
    def __init__(self):
        self.db = Database()  
        self.db.connect()     
        self.query = ConcertQueries(self.db)
        
    def get_all_concert_adi(self):
        return self.query.get_all_concert_ad()
    
    def get_concert_adi_populer(self):
        return self.query.get_all_concert_ad_populer()

    def get_soon_corcert_adi(self):
        return self.query.get_soon_concert_ad()
    
    def kategori_getir(self):
        return self.query.get_all_kategories()
    
    def kategoriye_gore_etkinli_getir(self,kategori_id):
        return self.query.kategoriye_gore_concert(kategori_id)
    
