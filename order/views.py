from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from order.models import ShopCart, ShopCartForm
from django.contrib import messages
from django.utils.crypto import get_random_string
from product.models import Category, Product


def index(request):
    return HttpResponse("Order App")





@login_required(login_url='/login')  # Giriş kontrolü
def addtocart(request, id):
    url = request.META.get('HTTP_REFERER')  # Son URL'yi al
    current_user = request.user
    checkproduct = ShopCart.objects.filter(product_id=id)

    if checkproduct:  # Ürün zaten sepette varsa kontrol değişkeni
        control = 1
    else:
        control = 0    # Ürün sepette yoksa kontrol değişkeni

    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.save(commit=False).quantity
                data.save()
                
            else:                 # Eğer ürün sepette yoksa, yeni bir ShopCart öğesi oluştur

                data = ShopCart()
                data.user = current_user
                data.product_id = id
                data.quantity = form.save(commit=False).quantity
                data.save()
                
            request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()              # Kullanıcının sepetindeki ürün sayısını güncelle

            messages.success(request, "Ürün başarı ile sepete eklenmiştir. Teşekkür ederiz")
            return HttpResponseRedirect(url)

    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id)              # Eğer ürün zaten sepette varsa, miktarı artır

            data.quantity += 1
            data.save()
        else:                        # Eğer ürün sepette yoksa, yeni bir ShopCart öğesi oluştur

            data = ShopCart()
            data.user = current_user
            data.product_id = id
            data.quantity = 1
            data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()          # Kullanıcının sepetindeki ürün sayısını güncelle

        messages.success(request, "Ürün başarı ile sepete eklenmiştir. Teşekkür ederiz")
        return HttpResponseRedirect(url)

    messages.warning(request, "Ürün sepete eklemede hata!")       # Eğer yukarıdaki koşulların hiçbiri sağlanmazsa, bir hata mesajı göster

    return HttpResponseRedirect(url)



@login_required(login_url='/login') # LOGİN YAPMAK GEREKLİ 
def shopcart(request):
    category = Category.objects.all() # TÜM ÜRÜNLERİ ÇEK 
    current_user = request.user  # USER GİRİŞ YAPTIMI 
    schopcart = ShopCart.objects.filter(user_id=current_user.id)   # Kullanıcının sepetindeki ürünleri filtrele
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count() # Kullanıcının sepetindeki ürün sayısını güncelle 
    total=0 # Toplam tutarı hesaplamak için bir değişken başlat
    for rs in schopcart:  # Sepetteki her ürün için döngü 
        total += rs.product.price * rs.quantity      # Her bir ürünün toplam fiyatını hesapla ve toplam değişkenine ekle

    #return HttpResponse(str(total))
    context={'schopcart': schopcart,
             'category':category,
             'total': total,
             }
    return render(request,'Shopcart_products.html',context)               
    
 
 
@login_required(login_url='/login') # KULLANICI GİRİŞ YAPMALI 
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()   # Verilen id'ye sahip olan ürünü sepetten sil 
    current_user=request.user # Güncel kullanıcıyı al 
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()     # Kullanıcının sepetinde kaç ürün olduğunu hesapla ve session'da sakla

    messages.success(request, "Ürün sepetten silinmiştir.")
    return HttpResponseRedirect("/shopcart")
    
    