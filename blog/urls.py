from django.urls import path
from . import views 

# TODO : update and delete post routes create krne h or unke lie template bhi

urlpatterns = [
    path('', views.home, name="blog_home"),
    path('<slug:slug>/', views.post, name="post_detail"),
    path('create-post/', views.createPost, name="create_post"),
]   