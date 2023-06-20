from django.contrib import admin
from .models import Contact, VUser
# Register your models here.

class contactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'date','message']
    
class VUserAdmin(admin.ModelAdmin):
    list_display = ['ip', 'arrived_first', 'last_seen']

admin.site.register(Contact, contactAdmin)
admin.site.register(VUser, VUserAdmin)