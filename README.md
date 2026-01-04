# EczaneSistemi_Grup16
## Eczane Otomasyon Sistemi v5.2

  Bu proje, doktorlar, eczacılar ve hastalar arasındaki reçete ve ilaç akışını dijitalleştiren, Python tabanlı kapsamlı bir masaüstü uygulamasıdır. Nesne Yönelimli Programlama (OOP) prensipleri kullanılarak geliştirilmiş olup, modern bir arayüz ve yerel veritabanı yönetimi sunar.
  
### 🚀 Özellikler

-Çoklu Kullanıcı Rolü: Doktor, Eczacı ve Hasta için özelleştirilmiş paneller.


-Reçete Yönetimi: Doktorlar ilaç veritabanından seçim yaparak reçete oluşturabilir.


-Stok Takibi: Eczacı satışı onayladığında stok otomatik olarak düşer.


-PDF Çıktısı: Hastalar reçetelerini PDF formatında bilgisayarlarına indirebilir.


-Modern Arayüz: ttkbootstrap ile geliştirilmiş, Karanlık/Aydınlık mod destekli kullanıcı dostu GUI.


-Raporlama: Eczacılar için anlık ciro ve satış raporları.

### 🛠️ Kullanılan Teknolojiler
-Dil: Python 3.x

-Arayüz (GUI): Tkinter & ttkbootstrap

-Veritabanı: SQLite3

-PDF İşlemleri: FPDF

### 📂 Proje Yapısı
EczaneOtomasyonu/
├── database.py         # Veritabanı bağlantısı ve CRUD işlemleri  

├── main.py             # Uygulamanın giriş noktası (Controller)

├── utils.py            # PDF oluşturma ve yardımcı araçlar

├── ui/                 # Kullanıcı Arayüzü Dosyaları

│   ├── login_panel.py      # Giriş Ekranı

│   ├── doctor_panel.py     # Doktor Paneli

│   ├── pharmacist_panel.py # Eczacı Paneli

│   └── patient_panel.py    # Hasta Paneli

└── database/           # Veritabanı dosyası (ilk çalıştırmada oluşur)
    └── eczane.db

### ⚙️ Kurulum
Projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

Repoyu klonlayın:
 ```bash 
  git clone https://github.com/efdalgzbyk/eczane-otomasyonu.git
  cd eczane-otomasyonu
```

Gerekli kütüphaneleri yükleyin:
```bash
  pip install ttkbootstrap fpdf
```

Uygulamayı başlatın:
```bash
  python main.py
```
