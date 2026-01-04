import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog

class PharmacistPanel:
    def __init__(self, parent, controller):
        self.controller = controller
        self.db = controller.db
        self.user = controller.active_user
        
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
        head = ttk.Frame(self.frame, bootstyle="primary", padding=10)
        head.pack(fill=X)
        ttk.Label(head, text=f"ECZACI: {self.user['ad_soyad']}", font=("Helvetica", 12, "bold"), bootstyle="inverse-primary").pack(side=LEFT)
        ttk.Button(head, text="ÇIKIŞ", bootstyle="danger", command=self.controller.show_login).pack(side=RIGHT)
        
        main = ttk.Frame(self.frame)
        main.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Sol: Reçeteler
        left = ttk.Labelframe(main, text="Reçeteler")
        left.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        self.tr_rec = ttk.Treeview(left, columns=("id", "ilac", "adet", "hasta"), show="headings")
        for c in ["id", "ilac", "adet", "hasta"]: self.tr_rec.heading(c, text=c.upper())
        self.tr_rec.pack(fill=BOTH, expand=True)
        
        bf = ttk.Frame(left)
        bf.pack(fill=X, pady=5)
        ttk.Button(bf, text="SEÇİLENİ VER", bootstyle=SUCCESS, command=self.process_sale).pack(side=LEFT, expand=True, fill=X, padx=2)
        ttk.Button(bf, text="İPTAL ET", bootstyle=DANGER, command=self.cancel_prescription).pack(side=LEFT, expand=True, fill=X, padx=2)
        
        # Sağ: Stoklar
        right = ttk.Labelframe(main, text="Stoklar")
        right.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
        self.tr_stok = ttk.Treeview(right, columns=("id", "ad", "stok", "fiyat"), show="headings")
        for c in ["id", "ad", "stok", "fiyat"]: self.tr_stok.heading(c, text=c.upper())
        self.tr_stok.pack(fill=BOTH, expand=True)
        
        bf2 = ttk.Frame(right)
        bf2.pack(fill=X, pady=5)
        ttk.Button(bf2, text="STOK ARTIR", bootstyle=INFO, command=self.increase_stock).pack(side=LEFT, expand=True, fill=X)
        ttk.Button(bf2, text="YENİ İLAÇ", bootstyle=PRIMARY, command=self.add_new_drug_popup).pack(side=LEFT, expand=True, fill=X)
        
        ttk.Button(main, text="SATIŞ RAPORU", bootstyle=WARNING, command=self.show_report).pack(side=BOTTOM, fill=X)
        
        self.refresh_data()

    def refresh_data(self):
        for t in [self.tr_rec, self.tr_stok]:
            for i in t.get_children(): t.delete(i)
        
        # Reçeteleri yükle
        pending = self.db.get_pending_prescriptions()
        for r in pending:
            self.tr_rec.insert("", "end", values=(r['id'], r['ad'], r['adet'], r['ad_soyad']))
        
        # İlaçları yükle
        drugs = self.db.get_all_drugs()
        for r in drugs:
            self.tr_stok.insert("", "end", values=(r['id'], r['ad'], r['stok'], r['fiyat']))

    def process_sale(self):
        sel = self.tr_rec.selection()
        if not sel: return
        rid = self.tr_rec.item(sel[0])['values'][0]
        
        # Stok kontrolü (Veri tekrar çekilir)
        pending = self.db.get_pending_prescriptions()
        item = next((x for x in pending if x['id'] == rid), None)
        
        if item and item['stok'] >= item['adet']:
            self.db.process_sale(rid, item['ilac_id'], item['adet'])
            messagebox.showinfo("Tamam", "İlaç Verildi")
            self.refresh_data()
        else:
            messagebox.showerror("Hata", "Stok Yetersiz")

    def cancel_prescription(self):
        sel = self.tr_rec.selection()
        if not sel: return
        if messagebox.askyesno("Onay", "İptal edilsin mi?"):
            rid = self.tr_rec.item(sel[0])['values'][0]
            self.db.delete_prescription(rid)
            self.refresh_data()

    def increase_stock(self):
        sel = self.tr_stok.selection()
        if not sel: return
        iid = self.tr_stok.item(sel[0])['values'][0]
        m = simpledialog.askinteger("Ekle", "Miktar")
        if m:
            self.db.update_stock(iid, m)
            self.refresh_data()

    def add_new_drug_popup(self):
        w = ttk.Toplevel()
        w.title("Yeni İlaç")
        w.geometry("300x300")
        ttk.Label(w, text="Ad:").pack(); e1 = ttk.Entry(w); e1.pack()
        ttk.Label(w, text="Fiyat:").pack(); e2 = ttk.Entry(w); e2.pack()
        ttk.Label(w, text="Stok:").pack(); e3 = ttk.Entry(w); e3.pack()
        
        def save():
            try:
                self.db.add_drug(e1.get(), e2.get(), e3.get())
                w.destroy()
                self.refresh_data()
            except: pass
        
        ttk.Button(w, text="Kaydet", command=save).pack(pady=10)

    def show_report(self):
        rep = ttk.Toplevel()
        rep.title("Rapor")
        rep.geometry("400x400")
        tr = ttk.Treeview(rep, columns=("ad", "ciro"), show="headings")
        tr.heading("ad", text="İlaç"); tr.heading("ciro", text="Ciro")
        tr.pack(fill=BOTH, expand=True)
        
        data = self.db.get_sales_report()
        total = 0
        for r in data:
            tr.insert("", "end", values=(r['ad'], f"{r['c']:.2f} TL"))
            total += r['c']
        
        ttk.Label(rep, text=f"TOPLAM: {total:.2f} TL", font=("bold", 12)).pack(pady=10)