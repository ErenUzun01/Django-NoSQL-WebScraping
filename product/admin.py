from django.contrib import admin
from django.utils.html import format_html
from djongo import models
from .models import Category, Product, Images
from mptt.admin import DraggableMPTTAdmin
from django.utils.safestring import mark_safe





class ProductImageInline(admin.TabularInline): 
    model = Images
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        # obj.image.url'e erişim uygun değil, Category modelinde bu alan yok
        return ''



class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'price', 'amount', 'image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [ProductImageInline]

    def image_tag(self, obj):
        if obj.image and obj.image.path:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />'.format(obj.image.url))
        return ''



class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'title', 'product']
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image and obj.image.path:
            return mark_safe('<img src="{}" height="50"/>'.format(obj.image.url))
        return ''

    image_tag.short_description = 'Image'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImagesAdmin)
