from database.database import Database
from database.userquerys import UserQueries
from database.concertquerys import ConcertQueries
from flask import Flask,render_template,redirect, url_for, request, make_response
 

# Create an instance of the Flask class
app = Flask(__name__)
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
    concert_data= datab.get_all_concert_ad()
    return render_template("index.html",concert_data=concert_data)
 
@app.route('/deneme')
def deneme():
    global db_instance 
    dbase = UserQueries(db_instance)
    users_data = dbase.get_all_users()

    if users_data is None:
        print("⚠️ HATA: Veritabanı sorgusu başarısız oldu. Loglara bakın.")
        users_data = [] 
    return render_template('deneme.html', users=users_data)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)