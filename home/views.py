from django.shortcuts import render, HttpResponse

# Create your views here.

def home(req):
    # return HttpResponse("this is home")
    return render(req, "base.html")

def contact(req):
    return render(req, "home/contact.html")

def about(req):
    return render(req, "home/about.html")

def handle(req, s):
    return HttpResponse(f"This is {s} that you typed in url")
