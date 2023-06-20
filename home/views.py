from django.shortcuts import render, redirect
from .forms import contactForm
from django.contrib import messages
from blog.models import Post
from django.db.models import Q
from .models import VUser
from django.utils import timezone
from django.db.models import Count 

def get_ip(req):
    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = req.META.get('REMOTE_ADDR')
    return ip


def home(req):
    # ! regiters new user to blog
    ip = get_ip(req)
    viewer, _ = VUser.objects.get_or_create(ip = ip)
    viewer.last_seen = timezone.now()
    viewer.save()
    posts = Post.objects.annotate(count = Count('viewers')).order_by('-count')[:10]
    return render(req, "home/home.html", {'posts':posts})

def contact(req):
    if req.method == 'POST':
        form = contactForm(req.POST)
        if form.is_valid():
            thread.sendMail(form).start()
            form.save()
            messages.info(req, f"Contact request recieved for {form.cleaned_data.get('name')}. Our team will contact you soon.")
            if not req.user.is_authenticated:
                return redirect('signin')
            return redirect("home")
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
    try:
        q = req.GET.get('query')
        if len(q) > 100 or len(q) < 3:
            posts = Post.objects.none()
            messages.error(req,"No results found. refine keywords")
        else:
            posts = Post.objects.filter(Q(title__icontains = q) | Q(description__icontains = q) | Q(content__icontains = q) | Q(author__first_name__icontains = q)| Q(author__last_name__icontains = q)| Q(categories__title__icontains = q)).order_by('-date_posted').distinct()
        return render(req, "blog/home.html", {'s':q, 'posts':posts})
    except:
        messages.error(req, "Some error occured while searching. Contact Lazy Coder Team.")
        return redirect("home")
