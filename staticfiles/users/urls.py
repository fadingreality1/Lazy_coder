from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import ResetPasswordForm, EnterNewPasswordForm, ChangePasswordForm

urlpatterns = [
    path('signup/', user_views.signup, name="signup"),
    path('signin/', user_views.signin, name="signin"),
    path('signout/', auth_views.logout_then_login, name="signout"),
    path('update/profile/', user_views.updateProfile, name="update_profile"),
    path('profile/user/<str:username>/', user_views.profile, name="profile"),
    path('user/profile/delete/', user_views.deleteUser, name="delete_profile"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'users/forgot_password.html', form_class = ResetPasswordForm), name = 'forgot_password'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html", form_class = EnterNewPasswordForm), name = 'password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_completed.html'), name = 'password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name = 'users/password_change.html', form_class=ChangePasswordForm, success_url = reverse_lazy("password_change_success")), name = 'change_password'),
    path('password-change/success/', user_views.PasswordChangeSuccess, name="password_change_success"),
    
]