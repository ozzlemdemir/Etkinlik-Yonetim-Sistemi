from app.database.ticketquerys import TicketQueries
from app.database.database import Database

class TicketService:
    def __init__(self):
        self.db = Database()  
        self.db.connect()     
        self.query = TicketQueries(self.db)
    def kisiye_gore_bilet_getir(self,id_user):
        return self.query.kisiye_gore_bilet(id_user)
    
    def yeni_bilet_ekle(self,user_id,etkinlik_id):
        return self.query.yeni_bilet(user_id,etkinlik_id)