from app.database.database import Database
class ConcertQueries:
    def __init__(self, db):
        self.db = db
        

    def get_all_concert_ad(self):
        query = 'SELECT "etkinlikAd","img","etkinlikID", "populer_mi" FROM etkinlik;'
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
            
            query_users = 'SELECT "userid" FROM biletler WHERE "etkinlikid" = %s;'
            kullanicilar = self.db.execute_query(query_users, (etkinlik_id,), fetch=True)
            mesaj = f"'{etkinlik_ad}' adlı etkinliğin bilgileri güncellenmiştir. Lütfen kontrol ediniz."
            print("deeneme")
            print(kullanicilar)
            
            if kullanicilar:
                query_notify = '''
                    INSERT INTO bildirimler (alici_id, gonderen_id, mesaj)
                    VALUES (%s, %s, %s);
                '''
                for k in kullanicilar:
                    alici_id = k[0]
                    self.db.execute_query(query_notify, (alici_id, 200, mesaj))#200 sistem yöneticisi id

            
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
    def for_admin_get_concert_by_id(self, concert_id=None):
        query = '''
            SELECT "etkinlikID", "etkinlikAd", img, kontenjan, tarih, adres, ucret, detay_bilgi
            FROM etkinlik
            WHERE "etkinlikID" = %s
        '''
        try:
            detay_konser = self.db.execute_query(query, (concert_id,), fetch=True, fetch_mode="one")
            return detay_konser if detay_konser is not None else []
        except Exception as e:
            print("Sorgu hatası:", e)
            self.db.conn.rollback()
            return []  
        
    def etkinlik_ekle(self,etkinlik_ad, img, kontenjan, tarih, adres, ucret, detay_bilgi,kategori_id):
        query="""INSERT INTO etkinlik ("etkinlikAd", "img", "kontenjan", "tarih", "adres", "ucret", "detay_bilgi", "kategoriid")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        try:
            self.db.execute_query(query,(etkinlik_ad, img, kontenjan, tarih, adres, ucret, detay_bilgi,kategori_id))
            self.db.conn.commit()
            print(f"Etkinlik '{etkinlik_ad}' başarıyla eklendi.")
            return True
        except Exception as e:
            print("Ekleme hatası:", e)
            self.db.conn.rollback()
            return False

    def add_kategori(self,kategori_ad):
        query="INSERT INTO kategori (kategori_adi) VALUES (%s)"
        try:
            self.db.execute_query(query, (kategori_ad,))
            self.db.conn.commit()
            print(f"Kategori '{kategori_ad}' başarıyla eklendi.")
            return True
        except Exception as e:
            print("Ekleme hatası:", e)
            self.db.conn.rollback()
            return False
        
        
    def populer_sayi(self):
        query = 'SELECT COUNT(*) FROM etkinlik WHERE populer_mi = TRUE;'
        result = self.db.execute_query(query, fetch=True)
        return result[0][0] if result else 0
    
    def populer_yap(self, etkinlik_id):
        query = '''
            UPDATE etkinlik 
            SET populer_mi = TRUE 
            WHERE "etkinlikID" = %s;
        '''
        try:
            self.db.execute_query(query, (etkinlik_id,))
            return True
        except Exception as e:
            print("Popüler yapma hatası:", e)
            self.db.conn.rollback()
            return False
        
    def populer_kaldir(self, etkinlik_id):
        query = '''
            UPDATE etkinlik 
            SET populer_mi = FALSE 
            WHERE "etkinlikID" = %s;
        '''
        try:
            self.db.execute_query(query, (etkinlik_id,))
            return True
        except Exception as e:
            print("Popüler kaldırma hatası:", e)
            self.db.conn.rollback()
            return False
        
    def etkinlik_click(self, user_id, etkinlik_id):
        query = """
            INSERT INTO event_clicks (user_id, etkinlik_id)
            VALUES (%s, %s)
        """
        self.db.execute_query(query, (user_id, etkinlik_id))
        
    def get_recommended_events(self, user_id):
        query = """
            SELECT e."etkinlikID", e."etkinlikAd", e.img, e.tarih, e.adres, COUNT(*) AS clicks
            FROM event_clicks ec
            JOIN etkinlik e ON e."etkinlikID" = ec.etkinlik_id
            LEFT JOIN biletler b ON b.etkinlikID = ec.etkinlik_id AND b.userid = %s
            WHERE ec.user_id = %s AND b.userid IS NULL
            GROUP BY e."etkinlikID", e."etkinlikAd", e.img, e.tarih, e.adres
            HAVING COUNT(*) >= 3
            ORDER BY clicks DESC
            LIMIT 5;
        """
        rows = self.db.execute_query(query, (user_id, user_id), fetch=True)
        return rows if rows else []