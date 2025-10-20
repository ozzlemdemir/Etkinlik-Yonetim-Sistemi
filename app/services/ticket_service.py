from app.database.ticketquerys import TicketQueries
from app.database.database import Database

class TicketService:
    def __init__(self):
        self.db = Database()  
        self.db.connect()     
        self.query = TicketQueries(self.db)
    def kisiye_gore_bilet_getir(self):
        return self.query.kisiye_gore_bilet()