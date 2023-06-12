from django.contrib import admin
from .models import Contact, VUser
# Register your models here.

class contactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'date','message']
    
class VUserAdmin(admin.ModelAdmin):
    list_display = ['ip', 'date_arrived_first']

admin.site.register(Contact, contactAdmin)
admin.site.register(VUser, VUserAdmin)