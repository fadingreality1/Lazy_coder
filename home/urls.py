from django.urls import path
from . import views as home_views

urlpatterns = [
    path('', home_views.home, name = 'home'),
    path('contact/', home_views.contact, name="contact" ),
    path('about/', home_views.about, name="about" ),
    path('search/', home_views.search, name="search"),
       
]