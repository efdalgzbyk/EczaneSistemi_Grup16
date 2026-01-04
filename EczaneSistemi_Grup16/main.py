import ttkbootstrap as ttk
from database import DatabaseManager
from ui.login_panel import LoginPanel
from ui.doctor_panel import DoctorPanel
from ui.patient_panel import PatientPanel
from ui.pharmacist_panel import PharmacistPanel

class EczaneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Eczane Otomasyonu v5.2 OOP")
        self.root.geometry("800x600")
        
        # Veritabanı Başlatma
        self.db = DatabaseManager()
        
        # Uygulama Durumu
        self.is_dark = False
        self.active_user = None
        
        self.show_login()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def toggle_theme(self):
        if self.is_dark:
            ttk.Style().theme_use("flatly")
            self.is_dark = False
        else:
            ttk.Style().theme_use("darkly")
            self.is_dark = True
        
        # Ekranı yenilemek için mevcut duruma göre yeniden çizim yapılabilir
        # Basitlik için login'e dönmüyoruz, sadece tema değişiyor.
        # Ancak kullanıcı o an hangi ekrandaysa o ekranın yeniden çizilmesi gerekebilir.
        # Bu örnekte tema değişimi sonrası login ekranına dönüyoruz:
        self.show_login()

    def show_login(self):
        self.clear_screen()
        self.root.geometry("400x550")
        self.active_user = None
        LoginPanel(self.root, self)

    def show_doctor_panel(self):
        self.clear_screen()
        self.root.geometry("650x750")
        DoctorPanel(self.root, self)

    def show_patient_panel(self):
        self.clear_screen()
        self.root.geometry("700x550")
        PatientPanel(self.root, self)

    def show_pharmacist_panel(self):
        self.clear_screen()
        self.root.geometry("1100x700")
        PharmacistPanel(self.root, self)

if __name__ == "__main__":
    root_window = ttk.Window(themename="flatly")
    app = EczaneApp(root_window)
    root_window.mainloop()