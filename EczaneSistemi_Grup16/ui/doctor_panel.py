import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter.ttk as std_ttk
from tkinter import messagebox

class DoctorPanel:
    def __init__(self, parent, controller):
        self.controller = controller
        self.db = controller.db
        self.user = controller.active_user
        
        self.frame = ttk.Frame(parent, padding=20)
        self.frame.pack(fill=BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
        head = ttk.Frame(self.frame, bootstyle="info", padding=10)
        head.pack(fill=X)
        ttk.Label(head, text=f"Dr. {self.user['ad_soyad']}", font=("Helvetica", 14, "bold"), bootstyle="inverse-info").pack(side=LEFT)
        ttk.Button(head, text="ÇIKIŞ", bootstyle="danger", command=self.controller.show_login).pack(side=RIGHT)

        frame = ttk.Labelframe(self.frame, text="Reçete Yaz", padding=20)
        frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Hasta Arama
        ttk.Label(frame, text="Hasta TC:").pack(anchor=W)
        f_src = ttk.Frame(frame)
        f_src.pack(fill=X, pady=5)
        self.ent_tc = ttk.Entry(f_src)
        self.ent_tc.pack(side=LEFT, expand=True, fill=X)
        self.lbl_st = ttk.Label(frame, text="...", foreground="gray")
        self.lbl_st.pack(anchor=W)
        
        self.active_hasta_id = None
        ttk.Button(f_src, text="Doğrula", bootstyle=INFO, command=self.find_patient).pack(side=RIGHT, padx=5)

        ttk.Separator(frame).pack(fill=X, pady=15)

        # İlaç Seçimi
        ttk.Label(frame, text="İlaç Ara & Seç:").pack(anchor=W)
        sv = ttk.StringVar()
        ent_search = ttk.Entry(frame, textvariable=sv)
        ent_search.pack(fill=X, pady=5)
        self.cb_drugs = std_ttk.Combobox(frame, state="readonly")
        self.cb_drugs.pack(fill=X, pady=5, ipady=4)
        
        # İlaçları Yükle
        all_d = self.db.get_all_drugs()
        self.d_list = [f"{d['ad']} (Stok:{d['stok']}) - {d['fiyat']} TL" for d in all_d]
        self.d_map = {d_str: all_d[i]['id'] for i, d_str in enumerate(self.d_list)}
        self.cb_drugs['values'] = self.d_list
        
        ent_search.bind("<KeyRelease>", lambda e: self.filter_drugs(sv))
        
        ttk.Label(frame, text="Adet:").pack(anchor=W, pady=10)
        self.ent_ad = ttk.Entry(frame)
        self.ent_ad.insert(0, "1")
        self.ent_ad.pack(fill=X)
        
        ttk.Button(frame, text="KAYDET", bootstyle=SUCCESS, command=self.save_prescription).pack(fill=X, pady=20)

    def find_patient(self):
        h = self.db.find_patient_by_tc(self.ent_tc.get())
        if h:
            self.active_hasta_id = h['id']
            self.lbl_st.config(text=f"✔ {h['ad_soyad']}", foreground="green")
        else:
            self.active_hasta_id = None
            self.lbl_st.config(text="❌ Bulunamadı", foreground="red")

    def filter_drugs(self, sv):
        val = sv.get().lower()
        filtered = [x for x in self.d_list if val in x.lower()]
        self.cb_drugs['values'] = filtered if filtered else ["Yok"]
        if filtered: self.cb_drugs.current(0)

    def save_prescription(self):
        if not self.active_hasta_id:
            messagebox.showerror("Hata", "Hasta seçin")
            return
        if not self.cb_drugs.get() or self.cb_drugs.get() not in self.d_map:
            messagebox.showerror("Hata", "İlaç seçin")
            return
        
        try:
            self.db.add_prescription(
                self.active_hasta_id, 
                self.user['id'], 
                self.d_map[self.cb_drugs.get()], 
                self.ent_ad.get()
            )
            messagebox.showinfo("Başarılı", "Reçete Yazıldı")
            self.ent_tc.delete(0, END)
            self.lbl_st.config(text="...")
            self.active_hasta_id = None
        except Exception as e:
            messagebox.showerror("Hata", str(e))