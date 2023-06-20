from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SigninForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Count
import os
from . import thread
from blog.models import Post

def signin(req):
    try:
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
    except Exception :
        messages.error(req, "Some error occured while signing in, contact the Lazy Coder Team")
        return redirect("home")
    
def signup(req):
    try:
        if req.method == "POST":
            form = UserRegisterForm(req.POST)
            if form.is_valid():
                form.save()
                thread.sendMail(form).start()
                var = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
                messages.success(req, f"Account created successfully for {var.title()}. You are signed in")
                new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'],)
                login(req, new_user)
                return redirect('profile', username = new_user.username)
            else:
                messages.warning(req, "There are some error in form you submitted. Kindly fill correct information.")
        else:
            form = UserRegisterForm()
        return render(req, "users/signup.html", {"form": form})
    
    except Exception as e:
        messages.error(req, "Some error occured while processing your data, please try again or contact Lazy Coder Team.")
        return redirect("home")
        
@login_required(login_url='signin')
def updateProfile(req):
    try: 
        if req.method == "POST":
            old_image = ''
            if req.user.profile.image:
                if os.path.isfile(req.user.profile.image.path):
                    old_image = req.user.profile.image.path
            u_form = UserUpdateForm(req.POST, instance=req.user)
            p_form = ProfileUpdateForm(req.POST, req.FILES, instance=req.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                if os.path.exists(old_image) and (req.FILES.get('image') != None or req.POST.get('image-clear') == 'on' ) :
                    os.remove(old_image)
                messages.success(req, f"Account Updated successfully for {req.user.first_name}.")
                return redirect('profile', username=req.user.username)
        else:   
            u_form = UserUpdateForm(instance=req.user)
            p_form = ProfileUpdateForm(instance=req.user.profile)
        return render(req, "users/update_profile.html",{'uform': u_form, 'pform':p_form})
    except Exception as e:
        messages.error(req, "Some error occured while updating your profile. kindly contact Lazy coder team or try again.")
        return redirect("home")

@login_required(login_url='signin')
def deleteUser(req):
    try:
        if req.user.profile.image:
                if os.path.isfile(req.user.profile.image.path):
                    os.remove(req.user.profile.image.path)
        User.objects.get(username = req.user).delete()
        messages.success(req, "account deleted successfully")
        return redirect('home')
    except:
        messages.error(req, "Some error occurred while deleting your account. Contact lazy coder team.")
        return redirect("home")

def profile(req, username):
    try:
        user = User.objects.get(username = username)
        all_posts = Post.objects.filter(author = user)
        likes = 0
        dislikes = 0
        views = 0
        category = []
        posts = all_posts.annotate(count = Count('likers')).order_by('-count')[:4]
        for p in all_posts:
            likes += p.likers.count()
            dislikes += p.dislikers.count()
            views += p.viewers.count()
            category += (p.categories.all())
        views = max(views, likes+dislikes)
        return render(req, "users/profile.html", {'user':user, 'posts':posts,'count':all_posts.count, 'likes':likes, 'dislikes':dislikes, 'views': views, 'category': set(category),})
    except Exception as e:
        messages.error(req, "Some Error occurred. No Such User Exists.")
        return redirect("home")
   
@login_required
def PasswordChangeSuccess(req):
    messages.success(req,"Your password has be chnaged successfully.")
    return redirect("profile", username=req.user.username)