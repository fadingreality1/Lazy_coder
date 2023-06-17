from django.shortcuts import render, HttpResponse, redirect
from .forms import contactForm
from django.contrib import messages
from blog.models import Post
from django.db.models import Q
from .models import VUser
from django.utils import timezone
from django.db.models import Count #? To add order by count facility which will help in trending as well as popular

# ! to capture ip address of viewer
def get_ip(req):
    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = req.META.get('REMOTE_ADDR')
    return ip


# ! implemented multithreading to make response faster
from . import thread
# Create your views here.


def home(req):
    # ! regiters new user to blog
    ip = get_ip(req)
    # if not VUser.objects.filter(ip = ip).exists():
    #     VUser(ip = ip).save()
    # else:
    #     o_user = VUser.objects.get(ip = ip)
    #     o_user.last_seen = timezone.now()
    #     o_user.save()
    
    # ? better method
    viewer, _ = VUser.objects.get_or_create(ip = ip)
    viewer.last_seen = timezone.now()
    viewer.save()
    # ? Accessing many to many field with annotate method 
    posts = Post.objects.annotate(count = Count('viewers')).order_by('-count')[:10]
    return render(req, "home/home.html", {'posts':posts})


def contact(req):
    if req.method == 'POST':
        form = contactForm(req.POST)
        if form.is_valid():
            
            # ! implemented multithreading to send mail and make response faster
            thread.sendMail(form).start()
            
            form.save()

            messages.info(req, f"Contact request recieved for {form.cleaned_data.get('name')}. Our team will contact you soon.")
            
            return redirect('signin')

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
        if len(q) > 100 or len(q) < 4:
            posts = Post.objects.none()
            messages.error(req,"No results found. refine keywords")
        else:
            posts = Post.objects.filter(Q(title__icontains = q) | Q(description__icontains = q) | Q(content__icontains = q) | Q(author__first_name__icontains = q)| Q(author__last_name__icontains = q)| Q(categories__title__icontains = q)).order_by('-date_posted').distinct()
        return render(req, "blog/home.html", {'s':q, 'posts':posts})
    except:
        messages.error(req, "Some error occured while searching. Contact Lazy Coder Team.")
        return redirect("home")
