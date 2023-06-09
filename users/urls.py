"""
URL configuration for Lazy_coder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', user_views.signup, name="signup"),
    path('signin/', auth_views.LoginView.as_view(template_name='users/signin.html'), name="signin"),
    path('signout/', auth_views.logout_then_login, name="signout"),
    path('profile/', user_views.profile, name="profile"),
    path('user-profile/delete', user_views.deleteUser, name="delete_profile"),
    
    # TODO : password manipulation routes to be edited
    # TODO : user profile view to be edited as well
    # TODO : seperate page to update and view profile data
    # TODO : profile page pr all posts done by user aengi.
]