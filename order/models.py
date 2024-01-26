from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from product.models import Product

class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"  # ÜRÜN BAŞLIĞI VE SAYIYI ÇEK
        #return self.product

    @property   # ÜRÜNÜN DEĞİŞTİRİLEBİLRİ VE DOĞRUDNA OKUNABİLİRLİK SAĞLMAASI
    def amount(self): 
        return (self.quantity * self.product.price)    # KAÇ TANE ÜRÜN VAR * ÜRÜNÜN FİYATI  YANİ TOTAL
    
    
    @property
    def price(self):
        return (self.product.price) #  ÜRÜNÜN FİYATI
    
    
class ShopCartForm(ModelForm): # STOP CART MODEL ALINARAK ÜRÜNLERİN SAYILARINI ARTTIRMA AZALTMA İŞLEMİ
    class Meta:
        model = ShopCart
        fields = ['quantity']
     