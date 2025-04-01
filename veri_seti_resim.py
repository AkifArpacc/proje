import os
import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def klasoru_kontrol_et():
    """ 'resimler' klasörünü kontrol eder, yoksa oluşturur. """
    klasor = "resimler"
    if not os.path.exists(klasor):
        os.makedirs(klasor)
    return klasor

def resim_yukle():
    """ Kullanıcının bilgisayarından resim yüklemesini sağlar. """
    dosya_yolu = filedialog.askopenfilename(filetypes=[("Resim Dosyaları", "*.png;*.jpg;*.jpeg")])
    if dosya_yolu:
        klasor = klasoru_kontrol_et()
        dosya_adi = os.path.basename(dosya_yolu)
        yeni_yol = os.path.join(klasor, dosya_adi)
        os.rename(dosya_yolu, yeni_yol)
        resim_listesi['values'] = resimleri_listele()
        messagebox.showinfo("Başarılı", "Resim başarıyla yüklendi!")

def resimleri_listele():
    """ 'resimler' klasöründeki tüm uygun uzantılı dosyaları listeler. """
    klasor = klasoru_kontrol_et()
    resimler = [f for f in os.listdir(klasor) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    return resimler

def sutun_ekle():
    """ Kullanıcının belirttiği sütun adını ekler ve yeni giriş alanları açar. """
    sutun_adi = sutun_giris.get()
    if sutun_adi:
        sutunlar.append(sutun_adi)
        sutun_giris.delete(0, tk.END)
        tk.Label(veri_cercevesi, text=sutun_adi).pack()
        giris_kutusu = tk.Entry(veri_cercevesi)
        giris_kutusu.pack()
        veri_kutulari[sutun_adi] = giris_kutusu
    else:
        messagebox.showwarning("Uyarı", "Lütfen bir sütun adı girin!")

def veriyi_kaydet():
    """ Seçilen resimle birlikte girilen verileri CSV dosyasına kaydeder. """
    secilen_resim = resim_listesi.get()
    if not secilen_resim:
        messagebox.showwarning("Uyarı", "Lütfen bir resim seçin!")
        return
    
    veri = {sutun: veri_kutulari[sutun].get() for sutun in sutunlar}
    if all(veri.values()):
        klasor_yolu = "veri_setleri"
        if not os.path.exists(klasor_yolu):
            os.makedirs(klasor_yolu)
        dosya_yolu = os.path.join(klasor_yolu, "resim_veri_seti.csv")
        dosya_var = os.path.isfile(dosya_yolu)
        
        with open(dosya_yolu, mode='a', newline='', encoding='utf-8') as dosya:
            basliklar = ["Resim Adı", "Resim Yolu"] + sutunlar
            yazici = csv.DictWriter(dosya, fieldnames=basliklar)
            if not dosya_var:
                yazici.writeheader()
            
            veri_kaydi = {"Resim Adı": secilen_resim, "Resim Yolu": os.path.join("resimler", secilen_resim)}
            veri_kaydi.update(veri)
            yazici.writerow(veri_kaydi)
            
        messagebox.showinfo("Başarılı", "Veri başarıyla kaydedildi!")
    else:
        messagebox.showwarning("Uyarı", "Tüm alanları doldurun!")

# Ana pencere
pencere = tk.Tk()
pencere.title("Resim Veri Seti Oluşturucu")

sutunlar = []
veri_kutulari = {}

# Resim Seçme Alanı
tk.Label(pencere, text="Resim Seç:").pack()
resim_listesi = ttk.Combobox(pencere, values=resimleri_listele())
resim_listesi.pack()
tk.Button(pencere, text="Resim Yükle", command=resim_yukle).pack()

# Sütun Ekleme Alanı
sutun_cerceve = tk.Frame(pencere)
sutun_cerceve.pack(pady=10)

tk.Label(sutun_cerceve, text="Sütun Adı:").pack(side=tk.LEFT)
sutun_giris = tk.Entry(sutun_cerceve)
sutun_giris.pack(side=tk.LEFT)
tk.Button(sutun_cerceve, text="Sütun Ekle", command=sutun_ekle).pack(side=tk.LEFT)

# Veri Girişi Alanı
veri_cercevesi = tk.Frame(pencere)
veri_cercevesi.pack(pady=10)

# Kaydet Butonu
tk.Button(pencere, text="Veriyi Kaydet", command=veriyi_kaydet).pack(pady=10)

pencere.mainloop()