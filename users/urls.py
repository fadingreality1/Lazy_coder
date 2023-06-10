from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', user_views.signup, name="signup"),
    path('signin/', user_views.signin, name="signin"),
    # ! not using that because i want to flash messages too.
    # path('signin/', user_views.Signin.as_view(), name="signin"),
    path('signout/', auth_views.logout_then_login, name="signout"),
    path('profile/', user_views.profile, name="profile"),
    path('user-profile/delete', user_views.deleteUser, name="delete_profile"),
 
    # TODO : password manipulation routes to be edited
    # TODO : user profile view to be edited as well
    # TODO : seperate page to update and view profile data
    # TODO : profile page pr all posts done by user aengi.
]