# Etkinlik Yönetim Sistemi


Bu proje, kullanıcıların çeşitli etkinlikleri (konser, tiyatro vb.) görüntüleyebileceği, bilet satın alabileceği ve yönetebileceği bir web uygulamasıdır. Flask tabanlı olarak geliştirilmiştir ve bir admin paneli ile etkinliklerin ve kullanıcıların yönetilmesine olanak tanır.

## Özellikler

Uygulama, kullanıcı ve admin olmak üzere iki temel rol için farklı yetenekler sunar.

### Kullanıcı Özellikleri
- **Kimlik Doğrulama:** Kayıt olma, giriş/çıkış yapma ve "Beni Hatırla" özelliği.
- **Etkinlik Keşfi:** Etkinlikleri listeleme, kategoriye göre filtreleme ve etkinlik detaylarını görüntüleme.
- **Bilet İşlemleri:** Etkinliklere bilet satın alma, ödeme simülasyonu, satın alınan biletleri görüntüleme ve iptal etme.
- **Profil Yönetimi:** Kullanıcı profili bilgilerini (isim, e-posta, şifre) güncelleme.
- **Güvenlik:** E-posta ile güvenli şifre sıfırlama.
- **Kişiselleştirme:** Kullanıcının gezdiği etkinliklere göre kişiselleştirilmiş "Öneriler" sayfası.
- **Bildirimler:** Admin tarafından yapılan etkinlik güncellemeleri gibi sistem bildirimlerini alma.

### Admin Özellikleri
- **Yönetim Paneli:** Toplam kullanıcı, etkinlik sayısı, bilet satışları gibi istatistiksel verileri gösteren bir dashboard.
- **Etkinlik Yönetimi:** Yeni etkinlik ekleme, mevcut etkinlikleri silme ve güncelleme (CRUD).
- **Kategori Yönetimi:** Sistem için yeni etkinlik kategorileri (örn: Konser, Tiyatro) ekleme.
- **Popüler Etkinlikler:** Anasayfada gösterilecek etkinlikleri "Popüler" olarak işaretleme ve kaldırma.
- **Profil Yönetimi:** Adminin kendi profil bilgilerini güvenli bir şekilde yönetmesi.

## Kullanılan Teknolojiler
- **Backend:** Python, Flask
- **Veritabanı:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript
- **Python Kütüphaneleri:**
  - `psycopg2`: PostgreSQL veritabanı bağlantısı için.
  - `bcrypt`: Güvenli şifre hashleme ve doğrulama.
  - `Flask-Mail`: Şifre sıfırlama özelliği için e-posta gönderimi.
  - `itsdangerous`: "Beni Hatırla" token'ları için güvenli veri serileştirme.

## Proje Yapısı

Proje, sorumlulukların ayrıldığı katmanlı bir mimari kullanır:

```
├── app/
│   ├── database/       # Veritabanı sorgularının bulunduğu katman
│   ├── services/       # İş mantığının bulunduğu servis katmanı
│   ├── static/         # CSS, JavaScript ve resim dosyaları
│   ├── templates/      # HTML şablonları (kullanıcı ve admin için ayrılmış)
│   ├── utils/          # Yardımcı fonksiyonlar (örn: rol kontrolü decorator'ı)
│   ├── __init__.py     # Flask uygulama fabrika fonksiyonu (create_app)
│   └── app_routes.py   # Tüm URL yönlendirmeleri
└── run.py              # Uygulamanın başlangıç noktası
```

## Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/ozzlemdemir/Etkinlik-Yonetim-Sistemi.git
    cd Etkinlik-Yonetim-Sistemi
    ```

2.  **Sanal Ortam Oluşturun ve Aktifleştirin:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Gerekli Paketleri Yükleyin:**
    ```bash
    pip install Flask psycopg2-binary bcrypt Flask-Mail itsdangerous
    ```

4.  **Veritabanını Ayarlayın:**
    -   PostgreSQL'de `EtkinlikApp` adında yeni bir veritabanı oluşturun.
    -   Veritabanı şemasını oluşturmak için SQL sorgularını çalıştırın. Gerekli tablolar: `users`, `etkinlik`, `biletler`, `kategori`, `event_clicks`, `password_resets`, `bildirimler`.

5.  **Veritabanı Bağlantısını Yapılandırın:**
    `app/database/database.py` dosyasındaki `__init__` metodunu kendi PostgreSQL bilgilerinizle güncelleyin:
    ```python
    def __init__(self, host="localhost", database="EtkinlikApp", user="postgres", password="sifreniz"):
        # ...
    ```

6.  **E-posta Ayarlarını Yapılandırın:**
    Şifre sıfırlama özelliğinin çalışması için `app/__init__.py` dosyasındaki `MAIL_` ile başlayan konfigürasyonları kendi SMTP sunucu bilgilerinizle güncelleyin.
     ```python
    app.config['MAIL_USERNAME'] = 'test@gmail.com'
    app.config['MAIL_PASSWORD'] = 'password'
    ```

7.  **Uygulamayı Çalıştırın:**
    ```bash
    python run.py
    ```

8.  Uygulamaya tarayıcınızdan `http://127.0.0.1:5000` adresi üzerinden erişebilirsiniz.
