import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import ImageTk, Image
import functions
import customtkinter
from collections import deque

class Queue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, data):
        self.queue.appendleft(data)

    def dequeue(self):
        return self.queue.pop()

    def is_empty(self):
        return len(self.queue) == 0
    
    def length(self):
        return len(self.queue)
    
    def ara_ve_sil(self, target):
        # Kuyruk içinde arama yap
        for item in self.queue:
            if item["Hisse_Kodu"] == target:
                self.queue.remove(item)
                return item  # İlgili öğeyi bulup sildiysek, öğeyi döndür
        return None  # Öğe bulunamadı


global kuyruk
kuyruk = Queue()


#arayüz genel özellikleri
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
root = customtkinter.CTk()
root.title("BorsAnaliz - 210101038")
root.iconbitmap("images/app.ico")
root.geometry("1600x900")
root.resizable(width="true", height="true")


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
favori_frame = customtkinter.CTkFrame(master=tabview.tab("Favoriler")).grid()


tree2 = ttk.Treeview(master=tabview.tab("Favoriler"))


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
        i += 1
        
    # Stil 
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 14), foreground="white", background="#122836")
    style.configure("Treeview.Heading", font=("Helvetica", 20), foreground="black", background="#122836", borderwidth=30)
    style.map("Treeview", foreground=[("selected", "white")], background=[("selected", "green")])

    # Treeview'ı göster
    tree1.grid(row=0, column=0, sticky="nsew")

fiyat_guncelle()

def favori_islem(islem):
    aranan_hisse = entry.get().upper() + " "
    found_data = functions.hisse_bul(aranan_hisse, islem)

    if found_data is None:
        messagebox.showerror("Hata", "Hisse bulunamadı")
    else:
        kuyruk.enqueue(found_data)
        print(kuyruk.length())
        tree_olustur()
       
def favori_islem_sil():
    silinecek_hisse = entry_favsil.get().upper() + " "

    print("Silinmeye çalışılan hisse:", silinecek_hisse)
    
    # Kuyruk verilerini göster test
    print("Kuyruk verileri:", kuyruk.queue)
    
    kuyruk.ara_ve_sil(silinecek_hisse)

    # Kuyruk verilerini göster test
    print("Kuyruk verileri:", kuyruk.queue)
    print(kuyruk.length())
    tree_olustur()
    

def tree_olustur():
        found_data = functions.hisse_bul("YEOTK ", "favEkle")
        # Treeview'ı temizle
        for item in tree2.get_children():
                tree2.delete(item)

        # Sütunları ayarla
        tree2["columns"] = tuple(found_data.keys())
        for column in tree2["columns"]:
            tree2.heading(column, text=column)
            tree2.column(column, anchor="center")

        # Veriyi ayrı sütunlara ekleyerek tree2'ye ekle
        i = 0
        for hisse in kuyruk.queue:
            tree2.insert("", i, values=tuple(hisse.values()))
            i += 1

        # Treeview'ı göster
        tree2.grid(row=0, column=0, sticky="nsew")
    
    
def portfoy_islem(islem):
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

entry_favsil = customtkinter.CTkEntry(master=tabview.tab("Favoriler"), placeholder_text="Hisse Adı Giriniz")
entry_favsil.grid(padx=10, pady=5)
fav_sil = customtkinter.CTkButton(master=tabview.tab("Favoriler"), text="sil", command=lambda: favori_islem_sil())
fav_sil.grid()

araya_eklenecek_bosluk = " " * 47
deger = araya_eklenecek_bosluk.join(["HİSSE", "FİYAT", "DEGİSİM"])
basliklar = customtkinter.CTkLabel(master=portfoy_frame, text=deger + "      " + "DEGER" + "      " + "KAR(TL)" + "    " + "KAR(%)", font=("Helvatica", 25), text_color="red")
basliklar.pack(side="top", fill="x")

my_image = customtkinter.CTkImage(light_image=Image.open("images/banner.png"),
                                  dark_image=Image.open("images/banner.png"),
                                  size=(1174, 281))

image_label = customtkinter.CTkLabel(master=frame_top, image=my_image, text="").pack(pady=20)
 

root.mainloop()
