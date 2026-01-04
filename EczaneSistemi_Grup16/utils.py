try:
    from fpdf import FPDF
    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False

def tr_fix(text):
    """PDF kütüphanesinin çökmemesi için Türkçe karakterleri dönüştürür"""
    if not text: return ""
    tr_map = {
        'ı': 'i', 'İ': 'I', 'ş': 's', 'Ş': 'S', 'ğ': 'g', 'Ğ': 'G',
        'ü': 'u', 'Ü': 'U', 'ö': 'o', 'Ö': 'O', 'ç': 'c', 'Ç': 'C'
    }
    for tr_char, eng_char in tr_map.items():
        text = text.replace(tr_char, eng_char)
    return text

def create_prescription_pdf(data, filename):
    if not HAS_FPDF:
        raise ImportError("fpdf kütüphanesi yüklü değil.")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, tr_fix("ECZANE RECETESI"), ln=1, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, tr_fix(f"Sayin: {data['ad_soyad']} (TC:{data['tc']})"), ln=1)
    pdf.cell(0, 10, tr_fix(f"Tarih: {data['tarih']}"), ln=1)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, tr_fix(f"ILAC: {data['ad']} - {data['adet']} Kutu"), ln=1)
    
    pdf.output(filename)