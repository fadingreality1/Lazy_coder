from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class SigninForm(AuthenticationForm):
    # ! To add custom class to all feilds of forms
    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'full-width'

class DateInput(forms.DateInput):
    input_type = 'date'

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, label="First name",required=True)
    last_name = forms.CharField(max_length=50, label="Last name",required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2',]
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
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {
            'date_of_birth': DateInput(),
        }
        fields = ['image','phone_number', 'date_of_birth', 'gender', 'address', 'profile_description']