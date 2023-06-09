from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SigninForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from Lazy_coder.settings import MEDIA_ROOT
import os

class Signin(auth_views.LoginView):
    form_class = SigninForm
    template_name = 'users/signin.html'
    # ! to pass form with custom classes added to it


def signup(req):
    if req.method == "POST":
        form = UserRegisterForm(req.POST)
        if form.is_valid():
            form.save()
            var = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
            
            messages.success(req, f"Account created successfully for {var.title()}. You are signed in")
            
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'],)
            login(req, new_user)
            return redirect('profile')
        else:
            messages.warning(req, "There are some error in form you submitted. Kindly fill correct information.")
    else:
        form = UserRegisterForm()
    # TODO: template bnani h users model k lie
    return render(req, "users/signup.html", {"form": form})


@login_required(login_url='signin')
def profile(req):
    if req.method == "POST":
        old_image = ''
        
        if req.user.profile.image:
            old_image = req.user.profile.image.path
        
        u_form = UserUpdateForm(req.POST, instance=req.user)
        p_form = ProfileUpdateForm(req.POST, req.FILES, instance=req.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            
            if os.path.exists(old_image) and req.POST.get('image') == None and old_image != f'{MEDIA_ROOT}'+'\\profile_pics\\default.png' :
                os.remove(old_image)
            
            messages.success(req, f"Account Updated successfully for {req.user.first_name}.")
            
            return redirect('profile')
    else:   
        u_form = UserUpdateForm(instance=req.user)
        p_form = ProfileUpdateForm(instance=req.user.profile)
    
    return render(req, "users/profile.html",{'uform': u_form, 'pform':p_form})


@login_required(login_url='signin')
def deleteUser(req):
    old = req.user.profile.image.path
    if old != f'{MEDIA_ROOT}'+'\\profile_pics\\default.png':
        os.remove(old)
    
    User.objects.get(username = req.user).delete()
    return redirect('blog_home')

