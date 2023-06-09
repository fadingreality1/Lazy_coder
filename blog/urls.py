from django.urls import path, include
from . import views as blog_views

urlpatterns = [
    path('', blog_views.home, name="blog_home"),
    path('post/<slug:slug>/', blog_views.post, name="post_detail")
]   