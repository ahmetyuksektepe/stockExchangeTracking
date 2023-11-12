from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import ttk
import functions
import customtkinter


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
root = customtkinter.CTk()
root.title("BorsAnaliz - 210101038")
root.iconbitmap("images/app.ico")
root.geometry("1600x900")
root.resizable(width="true", height="true")


data = functions.hisse_list
portfoy = []
favoriler = []

tabview = customtkinter.CTkTabview(master=root)
tabview.pack(expand=True, fill="both")

tabview.add("Ana Sayfa")  # add tab at the end
tabview.add("Hisse Performansı")  # add tab at the end
tabview.add("Portföy")
tabview.add("Favoriler")

favori_label = customtkinter.CTkLabel(master=tabview.tab("Favoriler"), text="")

text_label = customtkinter.CTkLabel(master=tabview.tab("Hisse Performansı"), text="Bir Hisse Seçin", font=("Helvetica", 30)).pack(pady=15)

frame_top = customtkinter.CTkFrame(master=tabview.tab("Ana Sayfa"))
frame_top.pack(fill="both")
frame_left = customtkinter.CTkFrame(master=tabview.tab("Ana Sayfa"), width=1600, height=300, fg_color="orange")
frame_left.pack()


def graph():
    functions.eski_veri()
    functions.cizim_yap(my_combo.get())


def fiyat_bilgisi():
    functions.hisse_temel()

    # Treeview'ı oluştur
    tree = ttk.Treeview(frame_left)
    tree["columns"] = tuple(functions.data[0].keys())

    # Sütun başlıklarını ayarla
    for column in tree["columns"]:
        tree.heading(column, text=column)
        tree.column(column, anchor="center")

    # Verileri ekley
    for i, hisse_verisi in enumerate(functions.data):
        tree.insert("", i, values=tuple(hisse_verisi.values()))

    # Stil tanımla
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 14), foreground="white", background="#122836")
    style.configure("Treeview.Heading", font=("Helvetica", 20), foreground="black", background="#122836", borderwidth=30)
    style.map("Treeview", foreground=[("selected", "white")], background=[("selected", "green")])

    # Treeview'ı göster
    tree.grid(row=0, column=0, sticky="nsew")

fiyat_bilgisi()

def favori_islem():
    functions.hisse_temel()

def portfoy_islem():
    pass


my_combo = customtkinter.CTkComboBox(master=tabview.tab("Hisse Performansı"), values=data,  height=50, width=150, corner_radius=30, border_width=2)
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

'''kategori_label = customtkinter.CTkLabel(master=tabview.tab("Ana Sayfa"), text_color="red", text="HİSSE        FİYAT       EN YÜKSEK      EN DÜŞÜK      DEĞİŞİM(%)             HACİM             SAAT", font=("Helvetica", 20), anchor="sw", padx=30, pady=30)
kategori_label.pack(padx=20, pady=20)
'''

yenile = customtkinter.CTkButton(master=tabview.tab("Ana Sayfa"), text="Verileri yenile", anchor="center", command=fiyat_bilgisi)
yenile.pack(padx=20, pady=20)


entry = customtkinter.CTkEntry(master=tabview.tab("Ana Sayfa"), placeholder_text="Hisse Adı Girin")
entry.pack(side="left")
favori_btn = customtkinter.CTkButton(master=tabview.tab("Ana Sayfa"), text="Favoriye Ekle", command=favori_islem)
favori_btn.pack( side="left")

entry2 = customtkinter.CTkEntry(master=tabview.tab("Ana Sayfa"), placeholder_text="Hisse Adı Girin")
entry2.pack(side="right")
ekle_btn = customtkinter.CTkButton(master=tabview.tab("Ana Sayfa"), text="Al", command=portfoy_islem)
ekle_btn.pack(side="right")

my_image = customtkinter.CTkImage(light_image=Image.open("images/bannertransparent.png"),
                                  dark_image=Image.open("images/bannertransparent.png"),
                                  size=(1174, 281))

image_label = customtkinter.CTkLabel(master=frame_top, image=my_image, text="").pack()
 

root.mainloop()