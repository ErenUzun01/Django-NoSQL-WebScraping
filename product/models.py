from djongo import models
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey

class Category(models.Model):
    STATUS_CHOICES = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    slug = models.SlugField(max_length=10, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    level = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title

   


class Product(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/', null=True)
    price = models.FloatField()
    amount = models.IntegerField()
    detail = RichTextUploadingField()
    slug = models.SlugField(max_length=150, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image and self.image.path:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        return ''


class Images(models.Model):
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
