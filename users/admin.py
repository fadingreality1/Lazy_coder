from django.contrib import admin
from .models import Profile

class AdminProfile(admin.ModelAdmin):
    list_display = ('get_username', 'get_f_name', 'get_l_name', 'phone_number')
    
    def get_username(self, obj):
        return obj.user.username
    
    def get_f_name(self, obj):
        return obj.user.first_name
    
    def get_l_name(self, obj):
        return obj.user.last_name
    
    get_l_name.admin_order_field = "user__last_name"
    get_f_name.admin_order_field = "user__first_name"
    get_username.admin_order_field = "user__username"
    
    get_l_name.short_description = "Last Name"
    get_f_name.short_description = "First Name"
    get_username.short_description = "Username"
    
admin.site.register(Profile, AdminProfile)