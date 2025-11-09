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

    def get_soon_concert_adi(self,user_id):
        return self.query.get_soon_concert_ad(user_id)
    
    def kategori_getir(self):
        return self.query.get_all_kategories()
    
    def kategoriye_gore_etkinli_getir(self,kategori_id):
        return self.query.kategoriye_gore_concert(kategori_id)
    
    def  etkinlik_getir_by_id(self,etkinlik_id):
        return self.query.get_concert_by_id(etkinlik_id)
    
    def update_concert(self, etkinlik_id, etkinlik_ad, img, kontenjan, tarih, adres, ucret, detay_bilgi):
        return self.query.update_concert(etkinlik_id, etkinlik_ad, img, kontenjan, tarih, adres, ucret, detay_bilgi)

    def delete_concert(self, etkinlik_id):
        return self.query.delete_concert(etkinlik_id)
    
    def for_admin_get_concert_by_id(self, etkinlik_id):
        return self.query.for_admin_get_concert_by_id(etkinlik_id)

    def for_admin_add_concert(self, etkinlik_ad, img, kontenjan, tarih, adres, ucret, detay_bilgi, kategori_id):
        return self.query.etkinlik_ekle(etkinlik_ad, img, kontenjan, tarih, adres, ucret, detay_bilgi, kategori_id)

    def for_admin_add_kategori(self,kategori_adi):
        return self.query.add_kategori(kategori_adi)
    
    def populer_yap(self, etkinlik_id):
        mevcut_sayi = self.query.populer_sayi()
        if mevcut_sayi >= 3:
            return False, "En fazla 3 etkinlik popüler olabilir!"
        self.query.populer_yap(etkinlik_id)
        return True, "Etkinlik popüler yapıldı."

    def populer_kaldir(self, etkinlik_id):
        self.query.populer_kaldir(etkinlik_id)
        return True, "Etkinlik popülerlikten çıkarıldı."
    
    
    
