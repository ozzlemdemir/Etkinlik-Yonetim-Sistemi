from app.database.database import Database
class ConcertQueries:
    def __init__(self, db):
        self.db = db
        

    def get_all_concert_ad(self):
        query = 'SELECT "etkinlikAd","img" FROM etkinlik;'
        concerts = self.db.execute_query(query, fetch=True)
        return concerts if concerts is not None else []
    
    def get_soon_concert_ad(self):
        query = 'SELECT e."etkinlikAd", e.img, b.satin_alma_tarihi FROM biletler b JOIN etkinlik e ON b.etkinlikID = e."etkinlikID" WHERE b.userid = 1 AND e.tarih < \'2027-11-19\' ORDER BY e.tarih ASC;'
        soonconcerts = self.db.execute_query(query, fetch=True)
        return soonconcerts if soonconcerts is not None else []
    
    def get_all_concert_ad_populer(self):
        query = 'SELECT "etkinlikAd","img" FROM etkinlik where "populer_mi"=True;'
        users = self.db.execute_query(query, fetch=True)
        return users if users is not None else []
    
    def get_all_kategories(self):
        query='SELECT * from kategori;'
        kategoriler=self.db.execute_query(query,fetch=True)
        return kategoriler if kategoriler is not None else []
        
    def kategoriye_gore_concert(self,kategori_id=None):
        query='SELECT e."etkinlikAd", e.img, k.kategori_adi FROM etkinlik e JOIN kategori k ON e.kategoriID = k.kategoriID WHERE e.kategoriID = %s'
        filtrelenmis_concert = self.db.execute_query(query, (kategori_id,), fetch=True)
        return filtrelenmis_concert if filtrelenmis_concert is not None else []
    
