from django.shortcuts import render, HttpResponse, redirect
from .models import Post
from django.contrib import messages
from django.db.models import Q
# Create your views here.

# TODO : Likes and views to be added in to model along with comments

def home(req):
    posts = Post.objects.all().order_by('-date_posted')
    return render(req, "blog/home.html", {'posts':posts})

def post(req, slug):
    try:
        post = Post.objects.get(slug = slug)
    except:
        messages.error(req, f"No such page exists for '{slug.replace('-', ' ')}'.")
        return redirect("home")
    
    return render(req, "blog/post.html", {'post':post,})
def createPost(req):
    return HttpResponse("create post called")