from flask import Blueprint, flash, render_template, redirect, url_for, request, make_response,jsonify,session
from app.services.concert_service import ConcertService
from app.services.ticket_service import TicketService
from app.services.user_service import UserService


app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def hello():
    return redirect(url_for('app_routes.login'))


@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        service = UserService()
        result = service.login(email, password)

        if result["success"]:
            user = result["user"]
            session["user_id"] = user[0]  # userID
            session["user_name"] = user[1]  # name
            session["role"] = result["role"]

            if result["role"] == "admin":
                flash("Admin girişi başarılı!", "success")
                return redirect(url_for("app_routes.admin_dashboard"))
            else:
                flash("Giriş başarılı!", "success")
                return redirect(url_for("app_routes.index"))

        else:
            flash(result["message"], "danger")
            return redirect(url_for("app_routes.login"))

    return render_template("login.html")

@app_routes.route('/admin_dashboard')
def admin_dashboard():
    name_admin=session.get("user_name")
    if session.get("role") != "admin":
        flash("Bu sayfaya erişim izniniz yok!", "danger")
        return redirect(url_for("app_routes.index"))
    return render_template("admin/admin_dashboard.html", name_admin=name_admin)

@app_routes.route("/register", methods=["GET", "POST"])
def register():
    user_service = UserService()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            flash("Şifreler uyuşmuyor!", "danger")
            return redirect(url_for("app_routes.register"))

        result = user_service.register(name, email, password)
        if result["success"]:
            flash("Kayıt başarılı! Giriş yapabilirsiniz.", "success")
            return redirect(url_for("app_routes.login"))
        else:
            flash(result["message"], "danger")# type: ignore
            return redirect(url_for("app_routes.register"))

    return render_template("register.html")

@app_routes.route('/logout')
def logout():
    session.clear()
    flash("Başarıyla çıkış yapıldı.", "info")
    return redirect(url_for("app_routes.login"))

@app_routes.route('/index')
def index():
    user_id=session.get("user_id")
    user_name = session.get("user_name")
    service = ConcertService()
    concert_data = service.get_concert_adi_populer()
    soon_concert=service.get_soon_concert_adi(user_id)
    return render_template("index.html",concert_data=concert_data,
                           soon_concert=soon_concert,
                           name_user=user_name,user_id=user_id
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
    user_id=session.get("user_id")
    service=TicketService()
    biletler=service.kisiye_gore_bilet_getir(user_id)
    return render_template("biletler.html", biletler=biletler)

@app_routes.route('/etkinlik_detay/<int:etkinlik_id>')
def etkinlik_detay(etkinlik_id):
    service=ConcertService()
    etkinlik = service.etkinlik_getir_by_id(etkinlik_id)
    return render_template('etkinlik_detay.html', etkinlik=etkinlik,etkinlik_id=etkinlik_id)

@app_routes.route('/bilet_al/<int:etkinlik_id>')
def bilet_al(etkinlik_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("Lütfen giriş yapın.", "danger")
        return redirect(url_for("app_routes.login"))

    ticketService = TicketService()
    mevcut_bilet = ticketService.kisiye_gore_bilet_var_mi(user_id, etkinlik_id)

    if mevcut_bilet:
        flash("Bu etkinlik için zaten bilet aldınız.", "warning")
        return redirect(url_for('app_routes.biletbyid'))
    else:
        return redirect(url_for('app_routes.bilet_odeme', etkinlik_id=etkinlik_id))
    
@app_routes.route('/bilet_odeme/<int:etkinlik_id>', methods=['GET', 'POST'])
def bilet_odeme(etkinlik_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("Lütfen giriş yapın.", "danger")
        return redirect(url_for('app_routes.login'))

    service = ConcertService()
    etkinlik = service.etkinlik_getir_by_id(etkinlik_id)

    if request.method == "POST":
        card_name = request.form.get('card_name')
        card_number = request.form.get('card_number')
        expiry = request.form.get('expiry')
        cvc = request.form.get('cvc')

        if not all([card_name, card_number, expiry, cvc]):
            flash("Lütfen tüm kart bilgilerini giriniz.", "danger")
            return redirect(request.referrer)

        ticketService = TicketService()
        success = ticketService.yeni_bilet_ekle(user_id, etkinlik_id)

        if success:
            flash("Bilet başarıyla satın alındı!", "success")
            return redirect(url_for('app_routes.biletbyid'))
        else:
            flash("Bilet alınamadı, lütfen tekrar deneyin.", "danger")
            return redirect(request.referrer)

    return render_template('bilet_odeme.html', etkinlik=etkinlik, user_id=user_id, etkinlik_id=etkinlik_id)


#admin routeleri 
@app_routes.route('/admin_etkinlikler')
def admin_tumetkinlikler():
    # Admin girişi yapılmış mı kontrol et
    if session.get("role") != "admin":
        flash("Bu sayfaya erişim izniniz yok!", "danger")
        return redirect(url_for("app_routes.login"))

    service = ConcertService()
    tumkonserler = service.get_all_concert_adi()
    return render_template("admin/admin_tum_etkinlikler.html", tumkonserler=tumkonserler)