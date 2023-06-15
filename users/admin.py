from django.contrib import admin
from .models import Profile
from blog.models import Post, User
from django.db.models import Count


class AdminProfile(admin.ModelAdmin):
    # TODO: make ordering by views, likes and dislikes
    list_display = ('get_username', 'get_full_name', 'get_post_count', )
    
    def get_username(self, obj):
        return obj.user.username
    
    def get_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    
    def get_post_count(self, obj):
        uname = obj.user.username
        user = User.objects.get(username = uname)
        return Post.objects.filter(author = user).count()
    
    
    get_post_count.short_description = "Posts"
    
    # def get_f_name(self, obj):
    #     return obj.user.first_name
    
    # def get_l_name(self, obj):
    #     return obj.user.last_name
    
    # get_l_name.admin_order_field = "user__last_name"
    # get_f_name.admin_order_field = "user__first_name"
    get_username.admin_order_field = "user__username"
    get_full_name.admin_order_field = "user__first_name"
    
    # get_l_name.short_description = "Last Name"
    # get_f_name.short_description = "First Name"
    
    get_username.short_description = "Username"
    get_full_name.short_description = "Name"
    
admin.site.register(Profile, AdminProfile)