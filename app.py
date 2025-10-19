from database.database import Database
from database.userquerys import UserQueries
from database.concertquerys import ConcertQueries
from database.ticketquerys import TicketQueries
from flask import Flask,render_template,redirect, url_for, request, make_response
 

# Create an instance of the Flask class
app = Flask(__name__)
global db_instance
db_instance = Database(
        host="localhost", 
        database="EtkinlikApp", 
        user="postgres", 
        password="samsun55" 
    )

db_instance.connect()
if db_instance.conn is not None:
        print("Test Sonucu: ✅ Bağlantı nesnesi (conn) oluşturuldu.")
        
@app.route('/')
def hello():
    return render_template("hello.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/index')
def index():
    global db_instance
    datab=ConcertQueries(db_instance)
    concert_data= datab.get_all_concert_ad_populer()
    soonconcert_data=datab.get_soon_concert_ad()
    return render_template("index.html",
                           concert_data=concert_data,
                           soon_concert=soonconcert_data
                           )
 
@app.route('/etkinlikler')
def tumetkinlikler():
    sorgu=ConcertQueries(db_instance)
    
    kategories=sorgu.get_all_kategories()
    veriler=sorgu.get_all_concert_ad()
    return render_template("tum_etkinlikler.html",
                           veriler=veriler,
                           kategories=kategories,
                           )

@app.route('/biletler')
def biletbyid():
    sorgu=TicketQueries(db_instance)
    biletler=sorgu.kisiye_gore_bilet()
    return render_template("biletler.html",biletler=biletler)


@app.route('/deneme')
def deneme():
    global db_instance 
    dbase = UserQueries(db_instance)
    users_data = dbase.get_all_users()

    if users_data is None:
        print(" Veritabanı sorgusu başarısız oldu. Loglara bakın.")
        users_data = [] 
    return render_template('deneme.html', users=users_data)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)