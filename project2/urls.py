from django import views
from home import views
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout
from order import views as orderviews



urlpatterns = [   #yönlendirme url yeri
    path('', include('home.urls')),
    path('hakkimizda/',views.hakkimizda, name='hakkimizda'),
    path('referanslar/',views.referanslar, name='referanslar'),
    path('iletisim/',views.iletisim, name='iletisim'),
    
    
    
    
    path('masaüstübilgisayar/',views.masaüstübilgisayar_products, name='masaüstübilgisayar_products'),
    path('dizüstübilgisayar/',views.dizüstübilgisayar_products, name='dizüstübilgisayar_products'),
    path('kulaklık/',views.kulaklık_products, name='kulaklık_products'),
    path('tablet/', views.tablet_products, name='tablet_products'),
    path('category/<int:id>/<slug:slug>', views.category_products, name='category_products'),
    path('telefon/',views.telefon_products, name='telefon_products'),
    path('oyunkonsolu/',views.oyunkonsolu_products, name='oyunkonsolu_products'), 
    path('product/<int:id>/<slug:slug>', views.product_detail, name='product_detail'),   # url deseni id ve sluga göre çekilir
    path('signup/',views.signup_view, name='signup_view'),
    path('search/',views.product_search, name='product_search'), # Search için ekledik
    path('search_auto/',views.product_search_auto, name='product_search_auto'), # Search için ekledik
    path('order/', include('order.urls')),
    
    path('shopcart/',orderviews.shopcart, name='shopcart'),
   

    
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('product/', include('product.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('logout/',views.logout_view, name='logout_view'),
    path('login/',views.login_view, name='login_view'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # setting dosyalarını 
