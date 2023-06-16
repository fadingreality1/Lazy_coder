from django import forms
from django.contrib.auth.forms import (
        UserCreationForm,
        AuthenticationForm,
        PasswordResetForm,
        SetPasswordForm,
        PasswordChangeForm,
    )
from django.contrib.auth.models import User
from .models import Profile


class SigninForm(AuthenticationForm):
    # ! To add custom class to all feilds of forms
    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'full-width'
            
# TODO : Format every file before pushing to github and launching the project

class DateInput(forms.DateInput):
    input_type = 'date'


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        max_length=50, label="First name", required=True)
    last_name = forms.CharField(
        max_length=50, label="Last name", required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'full-width'


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Email address", required=True)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'full-width'


class ProfileUpdateForm(forms.ModelForm):
    
    fb = forms.URLField(label="Facebook", required=False)
    insta = forms.URLField(label="Instagram", required=False)
    snap = forms.URLField(label="snapchat", required=False)
    
    class Meta:
        model = Profile
        widgets = {
            'date_of_birth': DateInput(),
        }
        fields = ['image', 'phone_number', 'date_of_birth', 'address', 'tagline', 'bio', 'gender', 'fb', 'insta', 'twitter', 'snap', 'github', 'website', 'linkedin']
        
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'full-width'
            
class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'full-width'


class EnterNewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(EnterNewPasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'full-width'
      
            
class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'full-width'