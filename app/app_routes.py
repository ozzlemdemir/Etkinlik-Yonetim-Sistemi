from flask import Blueprint, flash, render_template, redirect, url_for, request, make_response,jsonify,session

from app.services.concert_service import ConcertService
from app.services.ticket_service import TicketService
from app.services.user_service import UserService


app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def hello():
    return render_template("hello.html")


@app_routes.route("/login", methods=["GET", "POST"])
def login():
    user_service = UserService()
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        result = user_service.login(email, password)

        if result["success"]:
            user = result["user"]
            session["user_id"] = user[0]   # userID
            session["user_name"] = user[1] # name
            flash("Giriş başarılı!", "success")
            return redirect(url_for("app_routes.index"))
        else:
            flash(result["message"], "danger")
            return redirect(url_for("app_routes.login"))

    return render_template("login.html")


@app_routes.route('/index')
def index():
    user_name = session.get("user_name")
    service = ConcertService()
    concert_data =  service.get_concert_adi_populer()
    soon_concert=service.get_soon_corcert_adi()
    return render_template("index.html",concert_data=concert_data,
                           soon_concert=soon_concert,
                           name_user=user_name
                           )
@app_routes.route('/etkinlikler')
def tumetkinlikler():
    service = ConcertService()
    tumkonserler=service.get_all_concert_adi()
    kategoriler=service.kategori_getir()
    return render_template("tum_etkinlikler.html", 
                           tumkonserler=tumkonserler,
                           kategoriler=kategoriler)
    
@app_routes.route('/kategori/<int:kategori_id>')
def kategoriye_gore_etkinlik(kategori_id):
    service=ConcertService()
    etkinlikler = service.kategoriye_gore_etkinli_getir(kategori_id)
    return jsonify(etkinlikler)

@app_routes.route('/biletler')
def biletbyid():
    service=TicketService()
    biletler=service.kisiye_gore_bilet_getir()
    return render_template("biletler.html", biletler=biletler)

@app_routes.route('/etkinlik_detay/<int:etkinlik_id>')
def etkinlik_detay(etkinlik_id):
    service=ConcertService()
    etkinlik = service.etkinlik_getir_by_id(etkinlik_id)
    return render_template('etkinlik_detay.html', etkinlik=etkinlik)


