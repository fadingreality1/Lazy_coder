from django.shortcuts import render, HttpResponse, redirect
from .forms import contactForm
from django.contrib import messages
from blog.models import Post
from django.db.models import Q
from .models import VUser

# ! implemented multithreading to make response faster
from . import thread
# Create your views here.

# TODO: Redirect the user to login page if user is not authenticated after filling contact form

def home(req):
    ip = get_ip(req)
    if not VUser.objects.filter(ip = ip).exists():
        VUser(ip = ip).save()
    # return HttpResponse("this is home")
    return render(req, "home/home.html")


def contact(req):
    if req.method == 'POST':
        form = contactForm(req.POST)
        if form.is_valid():
            
            # ! implemented multithreading to send mail and make response faster
            thread.sendMail(form).start()
            
            form.save()

            messages.info(req, f"Contact request recieved for {form.cleaned_data.get('name')}. Our team will contact you soon.")
            
            return redirect('blog_home')

        messages.warning(req, "There are some errors in form that you have submitted. Please fill correct information")
        return render(req, "home/contact.html", {'form': form})

    if req.user.is_authenticated:
        form = contactForm(initial={'name': f"{req.user.first_name} {req.user.last_name}", 'email': f"{req.user.email}",})
    else:
        form = contactForm()
    return render(req, "home/contact.html", {'form': form})


def about(req):
    return render(req, "home/about.html")


def search(req):
    q = req.GET.get('query')
    # TODO : to make search useless for string less than 5 characters
    # TODO: Modifications such as order by popularity needed, by likes or views
    if len(q) > 100:
        posts = Post.objects.none()
        messages.error(req,"No results found.")
    else:
        posts = Post.objects.filter(Q(title__icontains = q) | Q(description__icontains = q) | Q(content__icontains = q) | Q(author__first_name__icontains = q)).order_by('-date_posted')
    return render(req, "blog/home.html", {'s':q, 'posts':posts})
    
    
# ! to capture ip address of viewer
def get_ip(req):
    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = req.META.get('REMOTE_ADDR')
    return ip
