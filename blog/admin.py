from django.contrib import admin
from .models import Post, Comment, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','get_category', 'date_posted', 'get_likes','get_dislikes','get_views',)
    
    def get_likes(self, obj):
        # ! converting to count to show at admin panel
        return obj.likers.count()
    
    get_likes.short_description = "Likes"
    get_likes.admin_order_field = "likers"
    
    def get_dislikes(self, obj):
        # ! converting to count to show at admin panel
        return obj.dislikers.count()
    
    get_dislikes.short_description = "Dislikes"
    get_dislikes.admin_order_field = "dislikers"
    
    def get_views(self, obj):
        # ! converting to count to show at admin panel
        return obj.viewers.count()
    
    get_views.short_description = "Views"
    get_views.admin_order_field = "viewers"
    
    # ! to access ManyToMany Related field
    def get_category(self, obj):
        
        category = [x for x in obj.categories.all()]
            
        return category
    
    get_category.short_description = "Categories"
    


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_post_title' ,'date_posted', 'content', 'parent','id',)
    
    def get_post_title(self, obj):
        return obj.post.title[:20]  
        
    get_post_title.admin_order_field = "post__title"
    get_post_title.short_description = "Post Title"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','id']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)


