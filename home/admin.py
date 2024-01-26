from django.contrib import admin
from .models import SettingDocument, ContactFormMessage

class SettingDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']
    readonly_fields = ('create_at', 'update_at')

admin.site.register(SettingDocument, SettingDocumentAdmin)

class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message', 'note', 'status']
    list_filter = ['status']

admin.site.register(ContactFormMessage, ContactFormMessageAdmin)
