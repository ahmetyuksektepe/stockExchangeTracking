from bs4 import BeautifulSoup
import requests,pandas,xlsxwriter
import os
import matplotlib.pyplot as plt
from collections import deque

URL = "https://borsa.doviz.com/hisseler"

klasor_yolu = r'D:\1\words\BilgisayarMuhendisligi\Sinif2\Donem1\veriyapilariproje\veriYapilari\bist100Gecmis' #başka bilgisayarlardaki bist100Gecmis'in dosya yoluyla güncellenebilir

# .xlsx dosyaları bul diziye ekle
dosya_isimleri = [dosya for dosya in os.listdir(klasor_yolu) if dosya.endswith('.xlsx')]

#plot çizim için sözlük yapısı
hisse_verileri_dict = {}

#kuyruk sınıfı
class Kuyruk:
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

    def hisse_kodu_ara(self, kodu):
        for hisse in self.queue:
            if hisse["Hisse_Kodu"] == kodu:
                return hisse
    
    def hisse_bilgi_al(self, kodu):
        for hisse in self.queue:
            if hisse["Hisse_Kodu"] == kodu:
                araya_eklenecek_bosluk = " " * 60
                deger = araya_eklenecek_bosluk.join([hisse["Hisse_Kodu"], hisse["Anlik fiyat"], hisse["Degisim:"]])
                return deger
        return None
    
    def hisse_fiyat_al(self, kodu):
        for hisse in self.queue:
            if hisse["Hisse_Kodu"] == kodu:
                return hisse["Anlik fiyat"]
        return None

kuyruk_verisi = Kuyruk()

def hisse_temel():
    global kuyruk_verisi 
    result = requests.get(URL)
    doc = BeautifulSoup(result.text, "html.parser")
    tbody = doc.tbody
    trs = tbody.find_all("tr")

    for tr in trs:
        td_list = tr.find_all("td")[1:7]
        if len(td_list) == 6:
            anlik, yuksek, dusuk, hacim, degisim, saat = td_list
            hisse_adi = tr['data-name'].split('-')
            hisse = {
                "Hisse Adi": hisse_adi[1],
                "Hisse_Kodu": hisse_adi[0],
                "Anlik fiyat": anlik.text.strip(),
                "Yuksek": yuksek.text.strip(),
                "Dusuk": dusuk.text.strip(),
                "Hacim": hacim.text.strip(),
                "Degisim:": degisim.text.strip(),
                "Saat": saat.text.strip()
            }
            kuyruk_verisi.enqueue(hisse)
    return kuyruk_verisi
#açılışta çalışması için
hisse_temel()

#hisse arama
def hisse_bul(aranan_hisse_kodu, islem):
    hisse_temel()
    bulunan_hisse = kuyruk_verisi.hisse_kodu_ara(aranan_hisse_kodu)
    
    if bulunan_hisse is not None: #önce ara
        
        if islem == "favEkle":
            return bulunan_hisse
        elif islem == "favSil":
            return bulunan_hisse
        elif islem == "prtEkle":
            hisse_isim = kuyruk_verisi.hisse_bilgi_al(aranan_hisse_kodu)
            return hisse_isim
        else:
            return "Bulunamadı"
    else:
        print(f"{bulunan_hisse} hisse koduna sahip hisse bulunamadı.")
        
def hisse_fiyat_bul(aranan_hisse_kodu):
    bulunan_hisse = kuyruk_verisi.hisse_fiyat_al(aranan_hisse_kodu)
    return bulunan_hisse

#Excelden eski verileri alır ve sözlük yapısı olarak kaydeder
def eski_veri():
    for hisse in dosya_isimleri:
        dosya_adi = hisse
        dosya_yolu = os.path.join('bist100Gecmis', dosya_adi)
        if os.path.exists(dosya_yolu):
            df = pandas.read_excel(dosya_yolu)
            hisse_verileri_dict[hisse + "_s1"] = df.iloc[::7, 0] #7şer 0. sütun
            hisse_verileri_dict[hisse + "_s2"] = df.iloc[::7, 1]
        else:
            print(f"{dosya_yolu} bulunamadı.")

#istenen hissenin grafiğini çizer
def cizim_yap(isim):
    x = hisse_verileri_dict[isim+ "_s1"]
    y = hisse_verileri_dict[isim+ "_s2"]

    # Scatter plot çizimi
    plt.plot(x, y, color='blue', linestyle='-', linewidth=2, label=isim)
    plt.xlabel("Tarih")
    plt.ylabel("Fiyat")
    plt.title(isim + " Fiyat Geçmişi")
   
    #for i, txt in enumerate(y):
      #  plt.annotate(txt, (x.iloc[i], y.iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.show()
    
