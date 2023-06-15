from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SigninForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from Lazy_coder.settings import MEDIA_ROOT
from django.db.models import Count
import os
from blog.models import Post

def signin(req):
    if req.method == "POST":
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            login(req, user)
            messages.success(req, f"You have signed in successfully as {user.first_name} {user.last_name}")
            return redirect('home')
        messages.error(req,"Invalid Credentials. Kindly fill correct information.")
        form = SigninForm(req.POST)
    else:
        form = SigninForm()
        
    return render(req, "users/signin.html", {'form':form})
    
# other way to signin but a longer method
# class Signin(auth_views.LoginView):
#     form_class = SigninForm
#     template_name = 'users/signin.html'
#     # ! to pass form with custom classes added to it


def signup(req):
    if req.method == "POST":
        form = UserRegisterForm(req.POST)
        if form.is_valid():
            form.save()
            var = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
            
            messages.success(req, f"Account created successfully for {var.title()}. You are signed in")
            
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'],)
            login(req, new_user)
            return redirect('profile', username = new_user.username)
        else:
            messages.warning(req, "There are some error in form you submitted. Kindly fill correct information.")
    else:
        form = UserRegisterForm()
    # TODO: template bnani h users model k lie
    return render(req, "users/signup.html", {"form": form})


@login_required(login_url='signin')
def updateProfile(req):
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


@login_required
def profile(req, username):
    # try:
        user = User.objects.get(username = username)
        all_posts = Post.objects.filter(author = user)
        likes = 0
        dislikes = 0
        views = 0
        category = []
        posts = all_posts.annotate(count = Count('likers')).order_by('-count')[:6]
        for p in all_posts:
            likes += p.likers.count()
            dislikes += p.dislikers.count()
            views += p.viewers.count()
            category += (p.categories.all())
        
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(category)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        views = max(views, likes+dislikes)
            
        return render(req, "users/profile.html", {'user':user, 'posts':posts,'count':all_posts.count, 'likes':likes, 'dislikes':dislikes, 'views': views, 'category': set(category),})
    # except Exception as e:
        messages.error(req, "Some Error occurred. No Such User Exists.")
        return redirect("home")