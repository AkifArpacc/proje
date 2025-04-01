import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def dosya_sec():
    # Kullanıcının Excel dosyasını seçmesi
    dosya_yolu = filedialog.askopenfilename(filetypes=[("Excel Dosyası", "*.xlsx;*.xls")])
    
    if dosya_yolu:
        # Excel dosyasını oku
        excel_dosyasi = pd.read_excel(dosya_yolu)
        
        # CSV dosyası için yol
        csv_yolu = "veri_setleri/veri_seti.csv"
        klasor_yolu = os.path.dirname(csv_yolu)
        
        # Klasör yoksa oluştur
        if not os.path.exists(klasor_yolu):
            os.makedirs(klasor_yolu)
        
        # Excel dosyasını CSV'ye dönüştür
        excel_dosyasi.to_csv(csv_yolu, index=False, encoding="utf-8")
        
        # Başarı mesajı
        messagebox.showinfo("Başarılı", "Excel dosyası başarıyla CSV formatına dönüştürüldü ve kaydedildi!")
    else:
        messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin!")

# Ana pencereyi oluştur
pencere = tk.Tk()
pencere.title("Excel'den CSV'ye Dönüştürücü")

# Dosya seçme butonu
buton = tk.Button(pencere, text="Excel Dosyasını Seç ve Dönüştür", command=dosya_sec)
buton.pack(pady=20)

# Ana döngü başlatma
pencere.mainloop()
