from django.urls import path, include
from . import views as blog_views

urlpatterns = [
    path('', blog_views.home, name="blog_home"),
]   