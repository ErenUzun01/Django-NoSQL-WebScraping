from bs4 import BeautifulSoup   # BeautifulSoup kütüphanesini projeye ekler. Bu kütüphane, HTML veya XML belgelerini çözümlemek için kullanılır.
import requests                 #kütüphanesini projeye ekler. Bu kütüphane, HTTP istekleri göndermek ve almak için kullanılır.
import pandas as pd             #Pandas kütüphanesini projeye ekler. Pandas, veri analizi ve manipülasyonu için sıkça kullanılan bir kütüphanedir.

url = "https://www.trendyol.com/tablet-x-c103665"  # Çekmek istediğim urlyi girdim 
response = requests.get(url)   # verdiğimiz url çalışıyormu kontrol   
html_icerigi = response.content  #html içeriği diye bir değişken
soup = BeautifulSoup(html_icerigi, "html.parser")  # veriyi çekiceğimiz kısımlar belirtilmesi soup değişkeni html içeriğini koyduk 

isim = soup.find_all("span", attrs="prdct-desc-cntnr-name hasRatings")   # HTML içeriğindeki tüm "span" elementlerini seçer ve belirli bir özelliğe ("prdct-desc-cntnr-name hasRatings") sahip olanları bulur.
fiyat = soup.find_all("div", attrs="prc-box-dscntd")                     #HTML içeriğindeki tüm "div" elementlerini seçer ve belirli bir özelliğe ("prc-box-dscntd") sahip olanları bulur.

liste = list()  #Bir liste oluşturur, bu liste içinde ürün isimleri ve fiyatları tutulacaktı

for i in range(len(isim)):  #İsim ve fiyat listeleri üzerinde döngü başlatır.
    isim[i] = (isim[i].text).strip("/n").strip()  # Her ürün adını alır ve başındaki ve sonundaki boşlukları temizler.
    fiyat[i] = (fiyat[i].text).strip("/n").strip()  #  Her fiyatı alır ve başındaki ve sonundaki boşlukları temizler.

    liste.append([isim[i], fiyat[i]])   # Temizlenmiş ürün adı ve fiyatını liste içine ekle

cikti = pd.DataFrame(liste, columns=["Ürün İsimleri", "Fiyatları"])   #Pandas DataFrame'ini oluşturur, bu DataFrame ürün isimleri ve fiyatları içerir.
print(cikti)



# Tablet url:  https://www.trendyol.com/tablet-x-c103665
# Dizüstü Bilgisayar url :  https://www.trendyol.com/sr?q=diz%C3%BCst%C3%BC%20bilgisayar&qt=diz%C3%BCst%C3%BC%20bilgisayar&st=diz%C3%BCst%C3%BC%20bilgisayar&os=1
# Masaüstü Bilgisayar url : https://www.trendyol.com/sr?q=masa%C3%BCst%C3%BC%20bilgisayar&qt=masa%C3%BCst%C3%BC%20bilgisayar&st=masa%C3%BCst%C3%BC%20bilgisayar&os=1
# Oyun Konsolu url : https://www.trendyol.com/sr?q=oyunkonsolu&qt=oyunkonsolu&st=oyunkonsolu&os=1&pi=3
# Kulaklık url : https://www.trendyol.com/sr?q=Kulakl%C4%B1k&qt=Kulakl%C4%B1k&st=Kulakl%C4%B1k&os=1
# Telefon url :  https://www.trendyol.com/sr?q=telefon&qt=telefon&st=telefon&os=1
