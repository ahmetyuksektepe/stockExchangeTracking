from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import ttk
import functions
import customtkinter

#arayüz genel özellikleri
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
root = customtkinter.CTk()
root.title("BorsAnaliz - 210101038")
root.iconbitmap("images/app.ico")
root.geometry("1600x900")
root.resizable(width="true", height="true")


#functions.hisse_temel() silinebilir
functions.eski_veri()
dosya_isim = functions.dosya_isimleri


tabview = customtkinter.CTkTabview(master=root)
tabview.pack(expand=True, fill="both")

tabview.add("Ana Sayfa")  # sona sekme ekle
tabview.add("Hisse Performansı")  # sona sekme ekle
tabview.add("Portföy")
tabview.add("Favoriler")

favori_label = customtkinter.CTkLabel(master=tabview.tab("Favoriler"), text="")

text_label = customtkinter.CTkLabel(master=tabview.tab("Hisse Performansı"), text="Bir Hisse Seçin", font=("Helvetica", 30)).pack(pady=15)

frame_top = customtkinter.CTkFrame(master=tabview.tab("Ana Sayfa"))
frame_top.pack(fill="both",  expand=True)
frame_left = customtkinter.CTkFrame(master=tabview.tab("Ana Sayfa"), width=1600, height=300, fg_color="orange")
frame_left.pack( expand=True)
portfoy_frame = customtkinter.CTkScrollableFrame(master=tabview.tab("Portföy"))
portfoy_frame.pack(fill="both", side="top", expand=True)


def graph():
    functions.cizim_yap(my_combo.get())

#BU KODU GÖZDEN GEÇİR
def fiyat_guncelle():
    # Kuyruk verilerini güncelle
    functions.kuyruk_verisi = functions.hisse_temel()
    
    #Treeview'ı oluştur
    tree1 = ttk.Treeview(frame_left)
    tree1["columns"] = tuple(functions.kuyruk_verisi.queue[0].keys())

    # Sütun başlıklarını ayarla
    for column in tree1["columns"]:
        tree1.heading(column, text=column)
        tree1.column(column, anchor="center")

    i = 0
    while not functions.kuyruk_verisi.is_empty():
        hisse = functions.kuyruk_verisi.dequeue()
        tree1.insert("", i, values=tuple(hisse.values()))
        print(hisse["Anlik fiyat"])
        i += 1
        
    # Stil tanımla
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 14), foreground="white", background="#122836")
    style.configure("Treeview.Heading", font=("Helvetica", 20), foreground="black", background="#122836", borderwidth=30)
    style.map("Treeview", foreground=[("selected", "white")], background=[("selected", "green")])

    # Treeview'ı göster
    tree1.grid(row=0, column=0, sticky="nsew")

fiyat_guncelle()

#her defasında son yazılanı ekliyor DÜZELTİLECEK
def favori_islem(islem):
    aranan_hisse = entry.get().upper() + " "
    functions.kuyruk_favori = functions.hisse_bul(aranan_hisse, islem)
    
    if functions.kuyruk_favori is None:
        messagebox.showerror("Hata", "Hisse bulunamadı")
    
    else:
        # Treeview'ı oluştur
        tree2 = ttk.Treeview(master=tabview.tab("Favoriler"))
        tree2["columns"] = tuple(functions.kuyruk_favori.queue[0].keys())

        # Sütun başlıklarını ayarla
        for column in tree2["columns"]:
            tree2.heading(column, text=column)
            tree2.column(column, anchor="center")
        
        # Stil tanımla
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 14), foreground="white", background="#122836")
        style.configure("Treeview.Heading", font=("Helvetica", 20), foreground="black", background="#122836", borderwidth=30)
        style.map("Treeview", foreground=[("selected", "white")], background=[("selected", "green")])
    
        if islem == "favEkle":
            i = functions.kuyruk_favori.length()
            while not functions.kuyruk_favori.is_empty():
                hisse = functions.kuyruk_favori.dequeue()
                tree2.insert("", i, values=tuple(hisse.values()))
                i -= 1
    
        # Treeview'ı göster
        tree2.grid(row=0, column=0, sticky="nsew")
    
    
    
def portfoy_islem(islem):
    #HİSSE ADI, GÜNCEL FIYATI VE KAR ZARAR ORANI YAZMALI
    aranan_hisse = entry2.get().upper() + " "
    hisse = functions.hisse_bul(aranan_hisse, islem)
    
    if hisse is None:
        messagebox.showerror("Hata", "Hisse bulunamadı")
        
    else:
        if islem == "prtEkle":
            fiyat = float(entry3.get())
            adet = float(entry4.get())
            maliyet = adet * fiyat
            guncel_deger = functions.hisse_fiyat_bul(aranan_hisse)
            kar =  float(guncel_deger.replace(',', '.')) * adet - maliyet 
            son_fiyat = float(guncel_deger.replace(',', '.')) * adet
            yuzde = (kar*100) / maliyet
            hisse_adi = customtkinter.CTkLabel(master=portfoy_frame, text=hisse + "          " + str(round(son_fiyat,2)) + "          " + str(round(kar, 2)) + "          %" + str(round(yuzde,2)), font=("Helvatica", 20))
            hisse_adi.pack(side="top", fill="x")
         

#



#tree 2


my_combo = customtkinter.CTkComboBox(master=tabview.tab("Hisse Performansı"), values=dosya_isim,  height=50, width=150, corner_radius=30, border_width=2)
my_combo.pack()

buton_simge = customtkinter.CTkImage(Image.open("images/line-chart.png"))
button = customtkinter.CTkButton(master=tabview.tab("Hisse Performansı"), 
                                 image=buton_simge,
                                 command=graph, 
                                 text="Grafiği Getir", 
                                 hover_color="green", 
                                 corner_radius=20, 
                                 width=200, 
                                 height=30, 
                                 border_spacing=10,
                                 font=("Helvetica", 20))
button.pack(padx=20, pady=20)

'''kategori_label = customtkinter.CTkLabel(master=portfoy_frame_top, text_color="red", text="HİSSE        FİYAT       EN YÜKSEK      EN DÜŞÜK      DEĞİŞİM(%)             HACİM             SAAT", font=("Helvetica", 20), anchor="sw", padx=30, pady=30)
kategori_label.pack(side="top", fill="both")'''


yenile = customtkinter.CTkButton(master=tabview.tab("Ana Sayfa"), text="Verileri yenile", anchor="center", command=fiyat_guncelle)
yenile.pack(padx=20, pady=20)


entry = customtkinter.CTkEntry(master=tabview.tab("Ana Sayfa"), placeholder_text="Hisse Adı Girin")
entry.pack(side="left")
favori_btn = customtkinter.CTkButton(master=tabview.tab("Ana Sayfa"), text="Favoriye Ekle", command=lambda: favori_islem("favEkle"))
favori_btn.pack( side="left")

entry2 = customtkinter.CTkEntry(master=tabview.tab("Ana Sayfa"), placeholder_text="Hisse Adı Girin")
entry3 = customtkinter.CTkEntry(master=tabview.tab("Ana Sayfa"), placeholder_text="Alış Fiyatını Giriniz")
entry4 = customtkinter.CTkEntry(master=tabview.tab("Ana Sayfa"), placeholder_text="Aldığınız Adedi Giriniz")
entry2.pack(side="right")
entry3.pack(side="right")
entry4.pack(side="right")
ekle_btn = customtkinter.CTkButton(master=tabview.tab("Ana Sayfa"), text="Al", command=lambda: portfoy_islem("prtEkle"))
ekle_btn.pack(side="right")

araya_eklenecek_bosluk = " " * 47
deger = araya_eklenecek_bosluk.join(["HİSSE", "FİYAT", "DEGİSİM"])
basliklar = customtkinter.CTkLabel(master=portfoy_frame, text=deger + "      " + "DEGER" + "      " + "KAR(TL)" + "    " + "KAR(%)", font=("Helvatica", 25), text_color="red")
basliklar.pack(side="top", fill="x")

my_image = customtkinter.CTkImage(light_image=Image.open("images/banner.png"),
                                  dark_image=Image.open("images/banner.png"),
                                  size=(1174, 281))

image_label = customtkinter.CTkLabel(master=frame_top, image=my_image, text="").pack(pady=20)
 

root.mainloop()
