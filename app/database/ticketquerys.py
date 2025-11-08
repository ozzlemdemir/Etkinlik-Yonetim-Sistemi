from app.database.database import Database
from datetime import datetime

class TicketQueries:
    def __init__(self, db_conn):
        self.db = db_conn
        
    def kisiye_gore_bilet(self,id_user):
        query = ' SELECT e."etkinlikAd", e.img, e.tarih, e.adres, e.ucret, b.satin_alma_tarihi, e."etkinlikID"  FROM biletler b JOIN etkinlik e ON b.etkinlikID = e."etkinlikID" WHERE b.userid = %s'
        try: 
            biletler = self.db.execute_query(query, params=(id_user,), fetch=True)
            
            formatted_biletler = []
            for bilet in biletler:
                satin_alma_tarihi = bilet[5].strftime("%d %B %Y, %H:%M")  
                formatted_biletler.append((
                    bilet[0],  # etkinlikAd
                    bilet[1],  # img
                    bilet[2],  # tarih
                    bilet[3],  # adres
                    bilet[4],  # ucret
                    satin_alma_tarihi , # biçimlendirilmiş tarih
                    bilet[6]  # etkinlikID
                ))
            
            return formatted_biletler if biletler is not None else []
        except Exception as e:
            print("Sorgu hatası:", e)
            self.db.conn.rollback()  
            return []
        
    def kisiye_gore_bilet_var_mi(self, user_id, etkinlik_id):
        sorgu = "SELECT * FROM biletler WHERE userid=%s AND etkinlikID=%s"
        mevcut_bilet = self.db.execute_query(sorgu, (user_id, etkinlik_id), fetch=True)
        return bool(mevcut_bilet)
    
    
    def yeni_bilet(self,user_id,etkinlik_id):
        query = "INSERT INTO biletler (userid, etkinlikID, satin_alma_tarihi) VALUES ( %s, %s, %s);"
        try:
            self.db.execute_query(query, (user_id, etkinlik_id, datetime.now()))
            return True
        except Exception as e:
            print("Bilet ekleme hatası:", e)
            self.db.conn.rollback()
            return False
        
    def bilet_sil(self,user_id,etkinlik_id):
        query1 = "DELETE FROM biletler WHERE userid=%s AND etkinlikID=%s;"
        query2 = "UPDATE etkinlik SET kontenjan = kontenjan + 1 WHERE \"etkinlikID\"=%s;"
        try:
            self.db.execute_query(query1, (user_id, etkinlik_id))
            self.db.execute_query(query2, (etkinlik_id,))
            return True
        except Exception as e:
            print("Bilet silme hatası:", e)
            self.db.conn.rollback()
            return False