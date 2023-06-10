from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'date_posted','slug',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_post_title' ,'date_posted', 'content')
    
    def get_post_title(self, obj):
        return obj.post.title   
    
    get_post_title.admin_order_field = "post__title"
    get_post_title.short_description = "Post Title"


    

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
