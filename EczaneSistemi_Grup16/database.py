import sqlite3
import os
import random
import datetime

class DatabaseManager:
    def __init__(self, db_file="database/eczane.db"):
        self.db_file = db_file
        if not os.path.exists("database"):
            os.makedirs("database")
        self.create_tables()
        self.insert_default_data()

    def connect(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def create_tables(self):
        conn = self.connect()
        c = conn.cursor()
        tables = [
            """CREATE TABLE IF NOT EXISTS kullanicilar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tc TEXT UNIQUE NOT NULL, ad_soyad TEXT DEFAULT 'Kullanıcı',
                sifre TEXT NOT NULL, tip TEXT NOT NULL)""",
            """CREATE TABLE IF NOT EXISTS ilaclar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT UNIQUE NOT NULL, fiyat REAL NOT NULL, stok INTEGER NOT NULL)""",
            """CREATE TABLE IF NOT EXISTS receteler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hasta_id INTEGER, doktor_id INTEGER, ilac_id INTEGER,
                adet INTEGER, tarih TEXT, verildi INTEGER DEFAULT 0,
                FOREIGN KEY(hasta_id) REFERENCES kullanicilar(id),
                FOREIGN KEY(doktor_id) REFERENCES kullanicilar(id),
                FOREIGN KEY(ilac_id) REFERENCES ilaclar(id))"""
        ]
        for t in tables: c.execute(t)
        conn.commit()
        conn.close()

    def insert_default_data(self):
        conn = self.connect()
        c = conn.cursor()
        users = [("11111111111", "Ahmet Eczacı", "1234", "Eczaci"),
                 ("22222222222", "Mehmet Hasta", "5678", "Hasta"),
                 ("33333333333", "Ayşe Doktor", "abcd", "Doktor")]
        for u in users:
            try: c.execute("INSERT INTO kullanicilar (tc,ad_soyad,sifre,tip) VALUES (?,?,?,?)", u)
            except: pass
        
        c.execute("SELECT count(*) FROM ilaclar")
        if c.fetchone()[0] == 0:
            drugs = [("Parol", 50), ("Majezik", 90), ("Augmentin", 140), ("Vermidon", 45), 
                     ("Dolorex", 70), ("A-ferin", 55), ("Gaviscon", 110), ("Levopront", 85)]
            for d in drugs:
                try: c.execute("INSERT INTO ilaclar (ad, fiyat, stok) VALUES (?,?,?)", (d[0], d[1], random.randint(10, 60)))
                except: pass
        conn.commit()
        conn.close()

    def login(self, tc, password):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM kullanicilar WHERE tc=? AND sifre=?", (tc, password))
        user = c.fetchone()
        conn.close()
        return user

    def register_user(self, tc, ad_soyad, sifre, tip):
        conn = self.connect()
        c = conn.cursor()
        c.execute("INSERT INTO kullanicilar (tc,ad_soyad,sifre,tip) VALUES (?,?,?,?)",
                  (tc, ad_soyad, sifre, tip))
        conn.commit()
        conn.close()

    def get_user_by_id(self, uid):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM kullanicilar WHERE id=?", (uid,))
        res = c.fetchone()
        conn.close()
        return res

    # --- Doktor Metotları ---
    def find_patient_by_tc(self, tc):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM kullanicilar WHERE tc=? AND tip='Hasta'", (tc,))
        res = c.fetchone()
        conn.close()
        return res

    def get_all_drugs(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM ilaclar ORDER BY ad")
        res = c.fetchall()
        conn.close()
        return res

    def add_prescription(self, hasta_id, doktor_id, ilac_id, adet):
        conn = self.connect()
        c = conn.cursor()
        c.execute("INSERT INTO receteler (hasta_id,doktor_id,ilac_id,adet,tarih) VALUES (?,?,?,?,?)",
                  (hasta_id, doktor_id, ilac_id, adet, str(datetime.date.today())))
        conn.commit()
        conn.close()

    # --- Hasta Metotları ---
    def get_patient_prescriptions(self, hasta_id):
        conn = self.connect()
        c = conn.cursor()
        c.execute("""SELECT r.id, i.ad, r.adet, r.tarih, r.verildi 
                     FROM receteler r JOIN ilaclar i ON r.ilac_id=i.id WHERE r.hasta_id=?""", (hasta_id,))
        res = c.fetchall()
        conn.close()
        return res

    def get_prescription_details(self, rid):
        conn = self.connect()
        c = conn.cursor()
        c.execute("""SELECT r.id, r.tarih, r.adet, i.ad, k.tc, k.ad_soyad
                     FROM receteler r JOIN ilaclar i ON r.ilac_id=i.id 
                     JOIN kullanicilar k ON r.hasta_id=k.id WHERE r.id=?""", (rid,))
        res = c.fetchone()
        conn.close()
        return res

    # --- Eczacı Metotları ---
    def get_pending_prescriptions(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute("""SELECT r.id, i.ad, r.adet, k.ad_soyad, r.ilac_id, i.stok 
                     FROM receteler r JOIN ilaclar i ON r.ilac_id=i.id 
                     JOIN kullanicilar k ON r.hasta_id=k.id WHERE r.verildi=0""")
        res = c.fetchall()
        conn.close()
        return res

    def process_sale(self, rid, ilac_id, adet):
        conn = self.connect()
        c = conn.cursor()
        # Stok kontrolü (Transaction güvenliği için tekrar kontrol edilebilir)
        c.execute("UPDATE ilaclar SET stok=stok-? WHERE id=?", (adet, ilac_id))
        c.execute("UPDATE receteler SET verildi=1 WHERE id=?", (rid,))
        conn.commit()
        conn.close()

    def delete_prescription(self, rid):
        conn = self.connect()
        c = conn.cursor()
        c.execute("DELETE FROM receteler WHERE id=?", (rid,))
        conn.commit()
        conn.close()
        
    def add_drug(self, ad, fiyat, stok):
        conn = self.connect()
        c = conn.cursor()
        c.execute("INSERT INTO ilaclar (ad,fiyat,stok) VALUES (?,?,?)", (ad, fiyat, stok))
        conn.commit()
        conn.close()

    def update_stock(self, ilac_id, amount):
        conn = self.connect()
        c = conn.cursor()
        c.execute("UPDATE ilaclar SET stok=stok+? WHERE id=?", (amount, ilac_id))
        conn.commit()
        conn.close()

    def get_sales_report(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT i.ad, SUM(r.adet*i.fiyat) as c FROM receteler r JOIN ilaclar i ON r.ilac_id=i.id WHERE r.verildi=1 GROUP BY i.ad")
        res = c.fetchall()
        conn.close()
        return res