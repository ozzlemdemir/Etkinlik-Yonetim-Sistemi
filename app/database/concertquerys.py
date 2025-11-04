from app.database.database import Database
class ConcertQueries:
    def __init__(self, db):
        self.db = db
        

    def get_all_concert_ad(self):
        query = 'SELECT "etkinlikAd","img","etkinlikID" FROM etkinlik;'
        try:
            concerts = self.db.execute_query(query, fetch=True)
            return concerts if concerts is not None else []
        except Exception as e:
            print("Sorgu hatası:", e)
            self.db.conn.rollback()  
            return []

    def get_soon_concert_ad(self,user_id):
        query = 'SELECT e."etkinlikID" , e."etkinlikAd", e.img, b.satin_alma_tarihi FROM biletler b JOIN etkinlik e ON b.etkinlikID = e."etkinlikID" WHERE b.userid = %s AND e.tarih < \'2027-11-19\' ORDER BY e.tarih ASC;'
        try:
            soonconcerts = self.db.execute_query(query, (user_id,), fetch=True)
            return soonconcerts if soonconcerts is not None else []
        except Exception as e:
            print("Sorgu hatası:", e)
            self.db.conn.rollback()  
            return []
    
    def get_all_concert_ad_populer(self):
        query = 'SELECT "etkinlikAd","img" ,"etkinlikID" FROM etkinlik where "populer_mi"=True;'
        try:
            users = self.db.execute_query(query, fetch=True)
            return users if users is not None else []
        except Exception as e:
            print("Sorgu hatası:", e)
            self.db.conn.rollback()  
            return []
    
    def get_all_kategories(self):
        query='SELECT * from kategori;'
        try:
            kategoriler=self.db.execute_query(query,fetch=True)
            return kategoriler if kategoriler is not None else []
        except Exception as e:
            print("Sorgu hatası:", e)
            self.db.conn.rollback()  
            return []
        
    def kategoriye_gore_concert(self,kategori_id=None):
        query='SELECT e."etkinlikAd", e.img,e."etkinlikID", k.kategori_adi FROM etkinlik e JOIN kategori k ON e.kategoriID = k.kategoriID WHERE e.kategoriID = %s'
        try:
            filtrelenmis_concert = self.db.execute_query(query, (kategori_id,), fetch=True)
            return filtrelenmis_concert if filtrelenmis_concert is not None else []
        except Exception as e:
            print("Sorgu hatası:", e)
            self.db.conn.rollback()  
            return []
    
    def get_concert_by_id(self,concert_id=None):
        query='SELECT "etkinlikAd", img, kontenjan, tarih, adres, ucret,detay_bilgi FROM etkinlik WHERE "etkinlikID"=%s'
        try:
            detay_konser = self.db.execute_query(query, (concert_id,), fetch=True, fetch_mode="one")#tek satır veri döndüğü için fetch==one dedik
            return detay_konser if detay_konser is not None else []
        except Exception as e:
            print("Sorgu hatası:", e)
            self.db.conn.rollback()  
            return []
    
        
    def update_concert(self, etkinlik_id, etkinlik_ad, img, kontenjan, tarih, adres, ucret, detay_bilgi):
        query = '''
            UPDATE etkinlik 
            SET "etkinlikAd" = %s, img = %s, kontenjan = %s, tarih = %s, adres = %s, ucret = %s, detay_bilgi = %s
            WHERE "etkinlikID" = %s;
        '''
        try:
            self.db.execute_query(query, (etkinlik_ad, img, kontenjan, tarih, adres, ucret, detay_bilgi, etkinlik_id))
            self.db.conn.commit()
            print(f"Etkinlik (ID: {etkinlik_id}) başarıyla güncellendi.")
            return True
        except Exception as e:
            print("Güncelleme hatası:", e)
            self.db.conn.rollback()
            return False


    def delete_concert(self, etkinlik_id):
        query = 'DELETE FROM etkinlik WHERE "etkinlikID" = %s;'
        try:
            self.db.execute_query(query, (etkinlik_id,))
            self.db.conn.commit()
            print(f"Etkinlik (ID: {etkinlik_id}) başarıyla silindi.")
            return True
        except Exception as e:
            print("Silme hatası:", e)
            self.db.conn.rollback()
            return False

    
