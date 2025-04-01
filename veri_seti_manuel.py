import os
import csv
import tkinter as tk
from tkinter import messagebox, simpledialog

def sutun_ekle():
    global sutunlar, veri_kutulari
    
    sutun_adi = sutun_giris.get().strip()
    if not sutun_adi:
        messagebox.showwarning("Uyarı", "Lütfen bir sütun adı girin!")
        return
    
    try:
        satir_sayisi = int(simpledialog.askstring("Satır Sayısı", 
                                f"'{sutun_adi}' sütunu için kaç özellik gireceksiniz?"))
        if satir_sayisi <= 0:
            raise ValueError
    except (ValueError, TypeError):
        messagebox.showwarning("Uyarı", "Lütfen geçerli bir sayı girin!")
        return
    
    # Arayüzü temizle (eski sütunları sil)
    for widget in veri_cercevesi.winfo_children():
        widget.destroy()
    
    # Yeni sütun bilgilerini güncelle
    sutunlar = [sutun_adi]
    veri_kutulari = {sutun_adi: []}
    
    # Yeni veri kutularını oluştur
    tk.Label(veri_cercevesi, text=sutun_adi, font=('Arial', 10, 'bold')).pack(pady=5)
    
    for i in range(satir_sayisi):
        frame = tk.Frame(veri_cercevesi)
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(frame, text=f"Özellik {i+1}:").pack(side=tk.LEFT)
        giris_kutusu = tk.Entry(frame)
        giris_kutusu.pack(side=tk.LEFT, expand=True, fill=tk.X)
        veri_kutulari[sutun_adi].append(giris_kutusu)
    
    sutun_giris.delete(0, tk.END)

def veriyi_kaydet():
    if not sutunlar:
        messagebox.showwarning("Uyarı", "Önce bir sütun ekleyin!")
        return
    
    # Tüm verileri topla (baştaki ve sondaki boşlukları temizle)
    yeni_kayit = {}
    for sutun in sutunlar:
        sutun_verileri = [kutu.get().strip() for kutu in veri_kutulari[sutun]]
        if not all(sutun_verileri):
            messagebox.showwarning("Uyarı", f"'{sutun}' sütunundaki tüm alanları doldurun!")
            return
        # Özellikleri tırnak içinde ve virgülle ayırarak birleştir
        yeni_kayit[sutun] = f'"{",".join(sutun_verileri)}"'
    
    klasor_yolu = "veri_setleri"
    if not os.path.exists(klasor_yolu):
        os.makedirs(klasor_yolu)
    dosya_yolu = os.path.join(klasor_yolu, "ogrenci_veri_seti.csv")
    
    # Mevcut verileri oku ve tüm sütunları al
    tum_sutunlar = []
    mevcut_veriler = []
    
    if os.path.exists(dosya_yolu):
        with open(dosya_yolu, mode='r', newline='', encoding='utf-8') as dosya:
            okuyucu = csv.DictReader(dosya)
            tum_sutunlar = okuyucu.fieldnames or []
            mevcut_veriler = list(okuyucu)
    
    # Eksik sütunları tamamla
    for sutun in tum_sutunlar:
        if sutun not in yeni_kayit:
            yeni_kayit[sutun] = ""
    
    # Tüm sütunları birleştir (eski ve yeni)
    tum_sutunlar = list(set(tum_sutunlar + sutunlar))
    
    # Yeni kaydı ekle
    mevcut_veriler.append(yeni_kayit)
    
    # CSV dosyasını güncelle
    with open(dosya_yolu, mode='w', newline='', encoding='utf-8') as dosya:
        yazici = csv.DictWriter(dosya, fieldnames=tum_sutunlar)
        yazici.writeheader()
        yazici.writerows(mevcut_veriler)
    
    messagebox.showinfo("Başarılı", "Veri başarıyla kaydedildi!")
    # Kayıt sonrası giriş kutularını temizle
    for sutun in veri_kutulari:
        for kutu in veri_kutulari[sutun]:
            kutu.delete(0, tk.END)

# Ana pencere
pencere = tk.Tk()
pencere.title("Öğrenci Veri Seti Oluşturucu")

sutunlar = []  # Sütun adlarını tutacak liste
veri_kutulari = {}  # Sütunlara ait giriş kutuları

# Sütun ekleme alanı
cerceve = tk.Frame(pencere)
cerceve.pack(pady=10)

tk.Label(cerceve, text="Sütun Adı:").pack(side=tk.LEFT)
sutun_giris = tk.Entry(cerceve)
sutun_giris.pack(side=tk.LEFT, padx=5)
tk.Button(cerceve, text="Sütun Ekle", command=sutun_ekle).pack(side=tk.LEFT)

# Verileri gireceğimiz alan
veri_cercevesi = tk.Frame(pencere)
veri_cercevesi.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

# Kayıt butonu
tk.Button(pencere, text="Verileri Kaydet", command=veriyi_kaydet).pack(pady=10)

# Ana döngü başlatma
pencere.mainloop()