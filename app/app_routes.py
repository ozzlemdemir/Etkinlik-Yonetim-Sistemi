from flask import Blueprint, render_template, redirect, url_for, request, make_response

from app.services.concert_service import ConcertService
from app.services.ticket_service import TicketService


app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def hello():
    return render_template("hello.html")


@app_routes.route('/login')
def login():
    return render_template("login.html")


@app_routes.route('/index')
def index():
    service = ConcertService()
    concert_data =  service.get_concert_adi_populer()
    soon_concert=service.get_soon_corcert_adi()
    return render_template("index.html",concert_data=concert_data,
                           soon_concert=soon_concert
                           )
@app_routes.route('/etkinlikler')
def tumetkinlikler():
    service = ConcertService()
    tumkonserler=service.get_all_concert_adi()
    kategoriler=service.kategori_getir()
    return render_template("tum_etkinlikler.html", tumkonserler=tumkonserler,
                           kategoriler=kategoriler)


@app_routes.route('/biletler')
def biletbyid():
    service=TicketService()
    biletler=service.kisiye_gore_bilet_getir()
    return render_template("biletler.html", biletler=biletler)
