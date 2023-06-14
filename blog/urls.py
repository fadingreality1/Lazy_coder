from django.urls import path
from . import views 

# TODO : update and delete post routes create krne h or unke lie template bhi

urlpatterns = [
    path('', views.home, name="blog_home"),
    path('create/post/', views.createPost, name="create_post"),
    path('post/like/', views.like, name="like_post"),
    path('post/dislike/', views.dislike, name="dislike_post"),
    path('post/category/<str:category>/', views.category, name="category_post"),
    path('post/delete/', views.delete, name="delete_post"),
    path('post/<slug:slug>/', views.post, name="post_detail"),
    path('post/<slug:slug>/update/', views.update, name="update_post"),
    path('post/<slug:slug>/post-comment/', views.postComment, name="post_comment"),
    path('post/<slug:slug>/<int:id>/delete-comment/', views.deleteComment, name="delete_comment"),
]   