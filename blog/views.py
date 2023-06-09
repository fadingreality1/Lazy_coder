from django.shortcuts import render, HttpResponse
from .models import Post
# Create your views here.

def home(req):
    posts = Post.objects.all().order_by('-date_posted')
    return render(req, "blog/home.html", {'posts':posts})