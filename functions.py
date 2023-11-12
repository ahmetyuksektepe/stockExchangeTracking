from bs4 import BeautifulSoup
import requests,pandas,xlsxwriter
import os
import matplotlib.pyplot as plt


URL = "https://borsa.doviz.com/hisseler"
RASYO_URL_TEMPLATE = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="

hisse_list = [
    "YEOTK",
    "EUPWR",
    "CWENE",
    "AKBNK",
    "KCHOL",
    "AKFYE",
    "AKFGY",
    "AKSA",
    "AKSEN",
    "AKCNS",
    "AHGAZ",
    "AEFES",
    "AGHOL",
    "ALBRK",
    "ISMEN",
    "KCHOL",
    "A1CAP",
    "ACSEL"
    ]
hisse_verileri_dict = {}

#Hissenin temel bilgilerini getirir
def hisse_temel():
    global data
    data = []
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
                "Hisse Adi":hisse_adi[1],
                "Hisse Kodu":hisse_adi[0],
                "Anlik fiyat":anlik.text.strip(),
                "Yuksek": yuksek.text.strip(),
                "Dusuk":dusuk.text.strip(),
                "Hacim":hacim.text.strip(),
                "Degisim:":degisim.text.strip(),
                "Saat":saat.text.strip(),
                # "F/K":rasyo_list[0],
                # "FD/FAVÖK":rasyo_list[1],
                # "PD/DD":rasyo_list[2],
                # "FD/Satışlar":rasyo_list[3],
                # "Yabancı Oranı (%)":rasyo_list[4],
                # "Ort Hacim (mn$) 3A/12A":rasyo_list[5],
                # "Piyasa Değeri":rasyo_list[6],
                # "Net Borç":rasyo_list[7],
                # "Yurtdışı Çarpan İskontosu (%)":rasyo_list[8],
                # "Halka Açıklık Oranı (%)":rasyo_list[9],
            }
            
            data.append(hisse)
    return data            

#Data'yı excele yazdırır
def excel_yazdir(data:list):
    df = pandas.DataFrame(data)
    writer = pandas.ExcelWriter("datas.xlsx",engine="xlsxwriter")
    df.to_excel(writer,sheet_name="Sheet1",index=False)
    writer.close()

def rasyo_degerleri(data:list):
    pass

def eski_veri():
    for hisse in hisse_list:
        dosya_adi = hisse + '.xlsx'
        dosya_yolu = os.path.join('bist100Gecmis', dosya_adi)
        if os.path.exists(dosya_yolu):
            df = pandas.read_excel(dosya_yolu)
            hisse_verileri_dict[hisse + "_s1"] = df.iloc[::7, 0]
            hisse_verileri_dict[hisse + "_s2"] = df.iloc[::7, 1]
        else:
            print(f"{dosya_yolu} bulunamadı.")



def eski_veri_cek(isim):
    hisse_adi = isim  
    if hisse_adi in hisse_verileri_dict:
        hisse_verileri = hisse_verileri_dict[hisse_adi]
        print(f"{hisse_adi} hissesinin verileri: {hisse_verileri}")
    else:
        print(f"{hisse_adi} hissesi bulunamadı.")

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
