from django.urls import path, include
from . import views as home_views

urlpatterns = [
    path('contact/', home_views.contact, name="contact" ),
    path('about/', home_views.about, name="about" ),
    path('<slug:s>', home_views.handle, name="handle"),
    # path('', home_views.handle, name="handle"),
    
    
]   