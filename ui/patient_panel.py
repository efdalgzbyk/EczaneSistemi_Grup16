import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
import utils

class PatientPanel:
    def __init__(self, parent, controller):
        self.controller = controller
        self.db = controller.db
        self.user = controller.active_user
        
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
        head = ttk.Frame(self.frame, bootstyle="success", padding=10)
        head.pack(fill=X)
        ttk.Label(head, text=f"Sn. {self.user['ad_soyad']}", font=("Helvetica", 12, "bold"), bootstyle="inverse-success").pack(side=LEFT)
        ttk.Button(head, text="ÇIKIŞ", bootstyle="danger", command=self.controller.show_login).pack(side=RIGHT)
        
        self.tree = ttk.Treeview(self.frame, columns=("id", "ilac", "adet", "tarih", "durum"), show="headings")
        headers = ["id", "ilac", "adet", "tarih", "durum"]
        for col in headers:
            self.tree.heading(col, text=col.upper())
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        self.load_data()
        
        ttk.Button(self.frame, text="SEÇİLENİ PDF OLARAK İNDİR", bootstyle=WARNING, command=self.download_pdf).pack(fill=X, padx=10, pady=10)

    def load_data(self):
        prescriptions = self.db.get_patient_prescriptions(self.user['id'])
        for r in prescriptions:
            durum = "ALINDI ✔" if r['verildi'] else "BEKLİYOR ⏳"
            self.tree.insert("", "end", values=(r['id'], r['ad'], r['adet'], r['tarih'], durum))

    def download_pdf(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Seç", "Lütfen bir reçete seçin")
            return
        
        rid = self.tree.item(sel[0])['values'][0]
        data = self.db.get_prescription_details(rid)
        
        fn = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if fn:
            try:
                utils.create_prescription_pdf(data, fn)
                messagebox.showinfo("Başarılı", f"PDF Kaydedildi:\n{fn}")
            except ImportError:
                messagebox.showwarning("Eksik", "fpdf kütüphanesi yok (pip install fpdf)")
            except Exception as e:
                messagebox.showerror("Hata", f"PDF hatası: {e}")