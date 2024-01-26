from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm, TextInput, Textarea

class SettingDocument(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    
    
    title = models.CharField(max_length=15)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True,max_length=150)
    phone = models.CharField(blank=True,max_length=15)
    fax = models.CharField(blank=True,max_length=15)
    email = models.CharField(blank=True,max_length=20)
    smtpserver = models.CharField(blank=True,max_length=20)
    smtpemail = models.CharField(blank=True,max_length=50)
    smtppassword = models.CharField(blank=True,max_length=10)
    smtpport = models.CharField(blank=True,max_length=5)
    icon = models.ImageField(blank=True, upload_to='images/')   #eklendi

    facebook = models.CharField(blank=True,max_length=50)
    instagram = models.CharField(blank=True,max_length=50)
    twitter = models.CharField(blank=True,max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact=RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
         ('Closed', 'Closed'),
        
    )
    name=models.CharField(blank=True,max_length=20)
    email = models.CharField(blank=True,max_length=50)
    subject = models.CharField(max_length=50, blank=True)
    message = models.CharField(max_length=255, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    ip = models.CharField(max_length=20, blank=True)
    note = models.CharField(max_length=100, blank=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    
class ContactFormu(ModelForm):
    class Meta:
        model=ContactFormMessage
        fields={'name','email','subject','message'}
        widgets={
            'name' : TextInput(attrs={'class': 'input','placeholder':'Name & Surname'}),      # FORM KISMI
            'email' : TextInput(attrs={'class': 'input','placeholder':'Email Address'}),
            'subject' : TextInput(attrs={'class': 'input','placeholder':'Subject'}),
            'message' : Textarea(attrs={'class': 'input','placeholder':'Your Message','rows':'5'}),
            
          
            
        }

   
    
    

    