from flask import Blueprint, flash, render_template, redirect, url_for, request, make_response,jsonify,session
import os
from werkzeug.utils import secure_filename
from app.services.concert_service import ConcertService
from app.services.ticket_service import TicketService
from app.services.user_service import UserService
from app.utils.decorators import role_required
from itsdangerous import URLSafeTimedSerializer
#cookie için serializer 
serializer = URLSafeTimedSerializer("SECRET_KEY")


app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def hello():
    return redirect(url_for('app_routes.login'))


@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember_me")

        service = UserService()
        result = service.login(email, password)

        if not result["success"]:
            flash(result["message"], "danger")
            return redirect(url_for("app_routes.login"))

        user = result["user"]
        session["user_id"] = user[0]
        session["user_name"] = user[1]
        session["role"] = result["role"]
        

        if remember:
            token = serializer.dumps(user[0])
            response = redirect(url_for("app_routes.index"))

            response.set_cookie(
                "remember_token",
                token,
                max_age=60*60*24*7,
                httponly=True,
                samesite="Lax"
            )

            UserService().kaydet_remember_token(user[0], token)
            flash("Beni Hatırla etkinleştirildi ✔", "info")
            return response

        if result["role"] == "admin":
            return redirect(url_for("app_routes.admin_dashboard"))
        else:
            return redirect(url_for("app_routes.index"))

    return render_template("login.html")




@app_routes.route('/admin_dashboard')
@role_required(["admin"])
def admin_dashboard():
    name_admin = session.get("user_name")
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
    response = redirect(url_for("app_routes.login"))
    response.delete_cookie("remember_token")
    flash("Başarıyla çıkış yapıldı.", "info")
    return redirect(url_for("app_routes.login"))

@app_routes.route('/index')
def index():
    user_id=session.get("user_id")
    user_name = session.get("user_name")
    
    if session.get("remember_login"):
        flash("Otomatik giriş yapıldı. Hoş geldiniz! 👋", "info")
        print("Otomatik giriş yapıldı.") #burası çalışmadı tekrar bak 
        session.pop("remember_login") 
    
    service = ConcertService()
    concert_data = service.get_concert_adi_populer()
    soon_concert=service.get_soon_concert_adi(user_id)
    return render_template("index.html",concert_data=concert_data,
                           soon_concert=soon_concert,
                           name_user=user_name,user_id=user_id
                           )
@app_routes.route('/etkinlikler')
@role_required(["user"])
def tumetkinlikler():
    service = ConcertService()
    tumkonserler=service.get_all_concert_adi()
    kategoriler=service.kategori_getir()
    return render_template("tum_etkinlikler.html", 
                           tumkonserler=tumkonserler,
                           kategoriler=kategoriler)
    
@app_routes.route('/kategori/<int:kategori_id>')
@role_required(["user"])
def kategoriye_gore_etkinlik(kategori_id):
    service=ConcertService()
    etkinlikler = service.kategoriye_gore_etkinli_getir(kategori_id)
    return jsonify(etkinlikler)

@app_routes.route('/biletler')
@role_required(["user"])
def biletbyid():
    user_id = session.get("user_id")
    service = TicketService()
    biletler = service.kisiye_gore_bilet_getir(user_id)
    return render_template("biletler.html", biletler=biletler)

@app_routes.route('/etkinlik_detay/<int:etkinlik_id>')
@role_required(["user"])
def etkinlik_detay(etkinlik_id):
    service = ConcertService()
    user_id=session.get("user_id")

    user_id = session.get("user_id") 
    service.etkinlik_click_kaydet(user_id, etkinlik_id)
    etkinlik = service.etkinlik_getir_by_id(etkinlik_id)

    return render_template(
        'etkinlik_detay.html',
        etkinlik=etkinlik,
        etkinlik_id=etkinlik_id
    )

@app_routes.route('/bilet_al/<int:etkinlik_id>')
@role_required(["user"])
def bilet_al(etkinlik_id):
    user_id = session.get("user_id")

    ticketService = TicketService()
    mevcut_bilet = ticketService.kisiye_gore_bilet_var_mi(user_id, etkinlik_id)

    if mevcut_bilet:
        flash("Bu etkinlik için zaten bilet aldınız.", "warning")
        return redirect(url_for('app_routes.biletbyid'))

    return redirect(url_for('app_routes.bilet_odeme', etkinlik_id=etkinlik_id))


@app_routes.route('/bilet_odeme/<int:etkinlik_id>', methods=['GET', 'POST'])
@role_required(["user"])
def bilet_odeme(etkinlik_id):
    user_id = session.get("user_id")

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

@app_routes.route('/bilet_iptal', methods=['POST'])
@role_required(["user"])
def bilet_iptal():
    user_id = session.get("user_id")
    etkinlik_id = request.form.get("etkinlik_id")

    ticketService = TicketService()
    success = ticketService.bilet_iptal_et(user_id, etkinlik_id)

    if success:
        flash("Bilet iptal edildi. Kartınıza iade sağlandı ✅", "success")
    else:
        flash("İptal sırasında hata oluştu.", "danger")

    return redirect(url_for('app_routes.biletbyid'))
 
@app_routes.route('/tum_etkinlikler_admin')
@role_required(["admin"])
def admin_tumetkinlikler():
    service = ConcertService()
    tumkonserler = service.get_all_concert_adi()
    return render_template("partials/admin_partial/admin_tum_etkinlikler.html", tumkonserler=tumkonserler)

@app_routes.route('/guncelle_etkinlik/<int:etkinlik_id>', methods=['GET', 'POST'])
@role_required(["admin"])
def guncelle_etkinlik(etkinlik_id):
    service = ConcertService()

    if request.method == 'POST':
        ad = request.form.get('ad')
        kontenjan = request.form.get('kontenjan')
        tarih = request.form.get('tarih')
        adres = request.form.get('adres')
        ucret = request.form.get('ucret')
        detay_bilgi = request.form.get('detay_bilgi')
        file = request.files.get('img')

        if file and file.filename:
            upload_folder = os.path.join('static', 'images')
            os.makedirs(upload_folder, exist_ok=True)
            save_path = os.path.join(upload_folder, file.filename)
            file.save(save_path)
            img_path = f"images/{file.filename}"
        else:
            mevcut_etkinlik = service.for_admin_get_concert_by_id(etkinlik_id)
            img_path = mevcut_etkinlik[2] if mevcut_etkinlik else None

        success = service.update_concert(
            etkinlik_id, ad, img_path, kontenjan, tarih, adres, ucret, detay_bilgi
        )

        if success:
            flash('Etkinlik başarıyla güncellendi!', 'success')
        else:
            flash('Etkinlik güncellenirken bir hata oluştu!', 'danger')

        return redirect(url_for('app_routes.admin_tumetkinlikler'))

    etkinlik = service.for_admin_get_concert_by_id(etkinlik_id)
    return render_template('partials/admin_partial/admin_guncelle_etkinlik.html', etkinlik=etkinlik)



@app_routes.route('/sil_etkinlik/<int:etkinlik_id>')
@role_required(["admin"])
def sil_etkinlik(etkinlik_id):
    service = ConcertService()
    success = service.delete_concert(etkinlik_id)

    if success:
        flash('Etkinlik başarıyla silindi.', 'success')
    else:
        flash('Etkinlik silinirken bir hata oluştu!', 'danger')

    return redirect(url_for('app_routes.admin_tumetkinlikler'))

@app_routes.route('/kategori_ekle', methods=['GET', 'POST'])
@role_required(["admin"])
def kategori_ekle():
    service = ConcertService()

    if request.method == 'POST':
        kategori_ad = request.form.get("kategori_ad")

        if kategori_ad:
            service.for_admin_add_kategori(kategori_ad)
            flash('Kategori başarıyla eklendi!', 'success')
            return redirect(url_for('app_routes.admin_dashboard'))
        else:
            flash('Lütfen kategori adını girin.', 'danger')

    return render_template('partials/admin_partial/admin_kategori_ekle.html')

@app_routes.route('/etkinlik_ekle', methods=['GET', 'POST'])
def etkinlik_ekle():
    service = ConcertService()

    # Veritabanındaki kategorileri al
    kategoriler = service.kategori_getir()

    if request.method == 'POST':
        etkinlik_ad = request.form.get("ad")
        kategori_id = request.form.get("kategori_id")
        img = request.files.get("img")
        kontenjan = request.form.get("kontenjan")
        tarih = request.form.get("tarih")
        adres = request.form.get("adres")
        ucret = request.form.get("ucret")
        detay_bilgi = request.form.get("detay_bilgi")

        if not img or img.filename == "":
            flash('Lütfen bir görsel seçin.', 'danger')
            return redirect(request.url)

        if etkinlik_ad and kategori_id and kontenjan and tarih and adres and ucret and detay_bilgi:
            filename = secure_filename(img.filename)  # type: ignore
            upload_folder = "app/static/uploads"
            os.makedirs(upload_folder, exist_ok=True)

            img.save(os.path.join(upload_folder, filename))
            db_img_path = f"images/{filename}"

            service.for_admin_add_concert(
                etkinlik_ad, db_img_path, kontenjan, tarih, adres, ucret, detay_bilgi, kategori_id
            )

            flash('Etkinlik başarıyla eklendi!', 'success')
            return redirect(url_for('app_routes.admin_dashboard'))
        else:
            flash('Lütfen tüm alanları doldurun.', 'danger')

    return render_template(
        'partials/admin_partial/admin_etkinlik_ekle.html',
        kategoriler=kategoriler
    )

@app_routes.route('/bildirimler')
@role_required(["user"])
def bildirimler():
    user_id = session.get("user_id")
    user_service = UserService()
    notifications = user_service.bildirimleri_getir(user_id)
    return jsonify(notifications)

#popüler etkinlik yapma ve kaldırma route'ları
@app_routes.route('/populer_yap/<int:etkinlik_id>')
@role_required(["admin"])
def populer_yap(etkinlik_id):
    service = ConcertService()
    success, message = service.populer_yap(etkinlik_id)

    if success:
        flash(message, "success")
    else:
        flash(message, "warning")

    return redirect(url_for('app_routes.admin_tumetkinlikler'))

@app_routes.route('/populer_kaldir/<int:etkinlik_id>')
@role_required(["admin"])
def populer_kaldir(etkinlik_id):
    service = ConcertService()
    success, message = service.populer_kaldir(etkinlik_id)

    flash(message, "success")
    return redirect(url_for('app_routes.admin_tumetkinlikler'))
