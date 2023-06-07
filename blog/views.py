from django.shortcuts import render, HttpResponse

# Create your views here.

def home(req):
    return render(req, "blog/home.html")