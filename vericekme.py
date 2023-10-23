from bs4 import BeautifulSoup
import requests

url = "https://borsa.doviz.com/hisseler"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

tbody = doc.tbody
trs = tbody.find_all("tr")


for tr in trs:
    td_list = tr.find_all("td")[1:7]
    if len(td_list) == 6:
        
        anlik, yuksek, dusuk, hacim, degisim, saat = td_list
        #Hisse Adını Hatalı Çektiği İçin değiştirdim
        # hisse_adi = anlik.find_next(class_="currency-details").text.strip()
        # hisse_adi = hisse_adi.split("\n")[0]
        # sirket_adi = anlik.find_next(class_="cname").text.strip()
        hisse_adi = tr['data-name']

        print("Hisse - Şirket Adı:", hisse_adi)
        print("Anlik fiyat:", anlik.text.strip())
        print("Yuksek:", yuksek.text.strip())
        print("Dusuk:", dusuk.text.strip())
        print("Hacim:", hacim.text.strip())
        print("Degisim:", degisim.text.strip())
        print("Saat:", saat.text.strip())
        print()
      
        
