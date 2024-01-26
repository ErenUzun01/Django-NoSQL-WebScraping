
from home.forms import SearchForm, SignUpForm
from home.models import SettingDocument,ContactFormu,ContactFormMessage
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from order.models import ShopCart
from product.models import Category, Images, Product
from django.shortcuts import get_object_or_404
from product.models import Product
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login


def index(request):
    setting = SettingDocument.objects.get(pk=1)  
    sliderdata = Product.objects.all()[:4]  # 4 tane ürün çektik hepsini çekmedik çünkü sistemi yormaya gerek yok.
    category=Category.objects.all()
    dayproducts = Product.objects.all()[:4]
    lastproducts = Product.objects.all().order_by('-id')[:4]
    randomproducts = Product.objects.all().order_by('-id')[8:12]
    current_user=request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    
    
    
    context = {'setting': setting,
               'category':category,
               'page': 'home',
               'sliderdata': sliderdata,
               'dayproducts':dayproducts,
               'lastproducts':lastproducts,
               'randomproducts':randomproducts,
               }
               
    return render(request, 'index.html', context)  

def hakkimizda(request):
    setting = SettingDocument.objects.get(pk=1)
    category = Category.objects.all()  
    context = {'setting': setting, 'category': category}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting = SettingDocument.objects.get(pk=1)
    categories = Category.objects.all()  # Category verilerini burada çekiyoruz.
    context = {'setting': setting, 'category': categories}
    return render(request, 'referanslarimiz.html', context)


def iletisim(request):
    if request.method == 'POST':
        form = ContactFormu(request.POST)      #İLETİŞİM MEDOTLARI OLUŞTURMA
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarı ile gönderilmiştir.Teşekkür ederiz") 
            return HttpResponseRedirect('/iletisim')

    setting = SettingDocument.objects.get(pk=1)
    form = ContactFormu()
    category = Category.objects.all() 

    context = {'setting': setting, 'form': form, 'category': category}

    return render(request, 'iletisim.html', context)






def category_products(request,id,slug):   # istediklerimizi alıyoruz
    category = Category.objects.all()  
    categorydata = Category.objects.get(pk=id)    #id ye göre çektik ürünleri
    products = Product.objects.all()   #products = Product.objects.filter(category_id=id)   bu masaüstü bilgisauarları gösteriyordu sadce burasu farklı 
    context = {'products': products,    
               'category':category,
               'categorydata':categorydata
               }
    
    return render(request, 'products.html', context)


def product_detail(request,id,slug):
    category = Category.objects.all()  
    product= Product.objects.get(pk=id)
    images=Images.objects.filter(product_id=id)
    context = {'product': product,
               'category':category,
               "images": images}
    
    return render(request, 'product_detail.html', context)




def tablet_products(request):
    # Tablet kategorisine ait ürünleri çektik
    tablet_products = Product.objects.filter(category__title='Tablet')

    # Görünüm  içeriği
    return render(request, 'products.html', {'products': tablet_products, 'categorydata': {'title': 'Tablet'}})


def masaüstübilgisayar_products(request):
    
    masaüstübilgisayar_products = Product.objects.filter(category__title='Masaüstü Bilgisayar')

  
    return render(request, 'products.html', {'products': masaüstübilgisayar_products, 'categorydata': {'title': ' Masaüstü Bilgisayar'}})

def dizüstübilgisayar_products(request):
   
    dizüstübilgisayar = Product.objects.filter(category__title='Dizüstü Bilgisayar')

   
    return render(request, 'products.html', {'products': dizüstübilgisayar, 'categorydata': {'title': ' Dizüstü Bilgisayar'}})



def kulaklık_products(request):
    
    kulaklık_products = Product.objects.filter(category__title='Kulaklık')
    
    return render(request, 'products.html', {'products': kulaklık_products, 'categorydata': {'title': 'Kulaklık'}})


def oyunkonsolu_products(request):
    
    oyunkonsolu_products = Product.objects.filter(category__title='Oyun Konsolu')

    
    return render(request, 'products.html', {'products': oyunkonsolu_products, 'categorydata': {'title': 'Oyunkonsolu'}})


def telefon_products(request):
    
    telefon_products = Product.objects.filter(category__title='Telefon')

    
    return render(request, 'products.html', {'products': telefon_products, 'categorydata': {'title': 'Telefon'}})


def product_search(request):
    if request.method == 'POST': # Post yani bir form gönderildiyse döner 
        form = SearchForm(request.POST)   # form adlı nesne oluşturduk    Seacrhform bir modül formu olmadığı için  forms.py adlı dosya oluşturup içine basit bir query nesnesi ekledik 
        if form.is_valid():   # Form geçerlimi değilmi?
            category = Category.objects.all()   #Katagori nesnelerini çek  
            query = form.cleaned_data['query'] # Formdan bilgiyi al 
            products=Product.objects.filter(title__icontains=query)  #  contains içermek demek  büyükharf küçük harfe karşılık  gelir i dersen farketmez          
            
            context = {'products': products, 
                       'category': category }
            return render(request, 'products_search.html', context)
        return HttpResponseRedirect('/')


import json

def product_search_auto(request):
    if request.is_ajax():    #AJAX isteği olup olmadığını kontrol et
        q = request.GET.get('term', '')  #GET parametrelerinden 'term' adındaki parametreyi al, yoksa boş bir string kullan
        products = Product.objects.filter(title__icontains=q) # Büyük küçük harf duyarlılıgını kapat

        results = [] # yeni sonuçları listele 
        for product in products:  # Filtrelenen ürünlerin bilgilerini JSON formatında bir liste oluştur
            product_json = {'id': product.id, 'label': product.title, 'value': product.title}  # Her bir ürün için JSON formatında bir nesne oluştur
            results.append(product_json)

        data = json.dumps(results)   # JSON formatındaki listeyi bir stringe çevir
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    else:
        data = 'fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


    

def logout_view(request): #ÇIKIŞ YAPMA
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':   
        username = request.POST.get("username")  # İSİM GİR 
        password = request.POST.get("password")   # ŞİFRE GİR
        if username and password:  # Kullanıcı adı ve şifre var mı kontrolü
            user = authenticate(request, username=username, password=password) # şifre  doğrumu isim doğrumu eşleşiyormu
            if user is not None: #  kullanıcı doğruysa giriş yap
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.warning(request, "Login Hatası! Kullanıcı adı veya şifre yanlış")  #yanlışsa hata mesajı
                return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'login.html', context)
       
       
       
def signup_view(request):   #signup formu 
    if request.method=='POST' :
        form=SignUpForm(request.POST)  #Kullanıcıdan verileri al
        if form.is_valid(): #Form geçerlimi?
            form.save()  #Formu kaydet 
            username=form.cleaned_data.get('username')   # kullanıcı adı şifreyi temizle 
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=password) #kullanıcıyı doğrula
            login(request,user) # kullanıcıya açık hale getir
            return HttpResponseRedirect('/')
    
    form=SignUpForm()   # Eğer HTTP isteği 'POST' değilse, yani sayfayı sadece görüntüleme isteği varsa signup formu oluştur
    category = Category.objects.all()  
    context = {'category': category,
               'form': form,}  
    return render(request, 'signup.html', context)