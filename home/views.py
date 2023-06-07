from django.shortcuts import render, HttpResponse, redirect
from .forms import contactForm

# Create your views here.

def home(req):
    # return HttpResponse("this is home")
    return render(req, "base.html")

def contact(req):
    if req.method == 'POST':
        form = contactForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_home')
        return render(req, "home/contact.html", {'form':form})
        
    form = contactForm()
    return render(req, "home/contact.html", {'form':form})

def about(req):
    return render(req, "home/about.html")

def handle(req, s):
    return HttpResponse(f"This is {s} that you typed in url")
