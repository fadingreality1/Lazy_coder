from django.contrib import admin
from .models import Profile
from blog.models import Post, User

# ! To display the fields in admin panel

class AdminProfile(admin.ModelAdmin):
    list_display = ('get_username', 'get_full_name', 'get_post_count', )
    
    # ! we cannot access data of other table directly, instead we have to use a get function for that
    # ! profile is one table and user is another.
    
    # ? here obj is profile object
    def get_username(self, obj):
        return obj.user.username
    
    def get_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    
    
    # ! Getting no. of blog posts made by any user.
    def get_post_count(self, obj):
        uname = obj.user.username
        user = User.objects.get(username = uname)
        return Post.objects.filter(author = user).count()
    

    # ? Name of column in admin panel
    get_post_count.short_description = "Posts"
    
    # ? Sorting k lie field
    get_username.admin_order_field = "user__username"
    get_full_name.admin_order_field = "user__first_name"
    
    get_username.short_description = "Username"
    get_full_name.short_description = "Name"

# ? Registering the display classes in admin panel along with model to show up in admin panel
admin.site.register(Profile, AdminProfile)