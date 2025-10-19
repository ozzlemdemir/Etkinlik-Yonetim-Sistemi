from database.database import Database
class TicketQueries:
    def __init__(self, db_conn):
        self.db = db_conn
        
    def kisiye_gore_bilet(self):
         query = 'SELECT e."etkinlikAd" ,e.img, b.satin_alma_tarihi FROM biletler b JOIN etkinlik e ON b.etkinlikID = e."etkinlikID" WHERE b.userid = 1;'
         biletler = self.db.execute_query(query, fetch=True)
         return biletler if biletler is not None else []
        
