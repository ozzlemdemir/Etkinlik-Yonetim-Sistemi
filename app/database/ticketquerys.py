from app.database.database import Database
from datetime import datetime

class TicketQueries:
    def __init__(self, db_conn):
        self.db = db_conn
        
    def kisiye_gore_bilet(self):
        query = ' SELECT e."etkinlikAd", e.img, e.tarih, e.adres, e.ucret, b.satin_alma_tarihi  FROM biletler b JOIN etkinlik e ON b.etkinlikID = e."etkinlikID" WHERE b.userid = 1'
          
        biletler = self.db.execute_query(query, fetch=True)
        
        formatted_biletler = []
        for bilet in biletler:
            satin_alma_tarihi = bilet[5].strftime("%d %B %Y, %H:%M")  
            formatted_biletler.append((
                bilet[0],  # etkinlikAd
                bilet[1],  # img
                bilet[2],  # tarih
                bilet[3],  # adres
                bilet[4],  # ucret
                satin_alma_tarihi  # biçimlendirilmiş tarih
            ))
        
        return formatted_biletler if biletler is not None else []