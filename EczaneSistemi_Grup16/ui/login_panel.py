import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class LoginPanel:
    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = ttk.Frame(parent, padding=20)
        self.frame.pack(fill=BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.frame, text="SİSTEM GİRİŞİ", font=("Helvetica", 18, "bold"), bootstyle="primary").pack(pady=30)
        
        ttk.Label(self.frame, text="TC Kimlik No:").pack(anchor=W)
        self.tc_ent = ttk.Entry(self.frame)
        self.tc_ent.pack(fill=X, pady=5)
        
        ttk.Label(self.frame, text="Şifre:").pack(anchor=W)
        self.pw_ent = ttk.Entry(self.frame, show="*")
        self.pw_ent.pack(fill=X, pady=5)
        
        self.lbl_msg = ttk.Label(self.frame, text="", foreground="red")
        self.lbl_msg.pack(pady=5)
        
        ttk.Button(self.frame, text="GİRİŞ YAP", bootstyle=PRIMARY, command=self.do_login).pack(fill=X, pady=10)
        ttk.Button(self.frame, text="KAYIT OL", bootstyle=SECONDARY, command=self.show_register_popup).pack(fill=X)
        
        mode_txt = "Aydınlık Mod ☀️" if not self.controller.is_dark else "Karanlık Mod 🌙"
        self.btn_theme = ttk.Button(self.frame, text=mode_txt, bootstyle="outline", command=self.toggle_theme_action)
        self.btn_theme.pack(pady=20)

    def toggle_theme_action(self):
        self.controller.toggle_theme()
        # Buton metnini güncellemek için paneli yenileyebiliriz veya direkt metni değiştirebiliriz
        new_txt = "Aydınlık Mod ☀️" if not self.controller.is_dark else "Karanlık Mod 🌙"
        self.btn_theme.configure(text=new_txt)

    def do_login(self):
        tc, pw = self.tc_ent.get(), self.pw_ent.get()
        user = self.controller.db.login(tc, pw)
        
        if user:
            self.controller.active_user = user
            if user['tip'] == "Doktor":
                self.controller.show_doctor_panel()
            elif user['tip'] == "Eczaci":
                self.controller.show_pharmacist_panel()
            else:
                self.controller.show_patient_panel()
        else:
            self.lbl_msg.config(text="Hatalı TC veya Şifre")

    def show_register_popup(self):
        reg = ttk.Toplevel()
        reg.title("Kayıt")
        reg.geometry("350x450")
        
        ttk.Label(reg, text="TC:").pack(pady=5)
        r_tc = ttk.Entry(reg); r_tc.pack(fill=X, padx=20)
        ttk.Label(reg, text="Ad Soyad:").pack(pady=5)
        r_ad = ttk.Entry(reg); r_ad.pack(fill=X, padx=20)
        ttk.Label(reg, text="Şifre:").pack(pady=5)
        r_pw = ttk.Entry(reg); r_pw.pack(fill=X, padx=20)
        ttk.Label(reg, text="Tip:").pack(pady=5)
        r_tip = ttk.Combobox(reg, values=["Hasta", "Doktor", "Eczaci"], state="readonly")
        r_tip.pack(fill=X, padx=20); r_tip.current(0)
        
        def save():
            try:
                self.controller.db.register_user(r_tc.get(), r_ad.get(), r_pw.get(), r_tip.get())
                messagebox.showinfo("Başarılı", "Kayıt yapıldı.")
                reg.destroy()
            except:
                messagebox.showerror("Hata", "TC zaten kayıtlı.")
        
        ttk.Button(reg, text="KAYDET", bootstyle=SUCCESS, command=save).pack(pady=20)