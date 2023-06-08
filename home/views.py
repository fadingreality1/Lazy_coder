from django.shortcuts import render, HttpResponse, redirect
from .forms import contactForm
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
# ! implemented multithreading to make response faster

from . import thread
# Create your views here.

# TODO: Redirect the user to login page if user is not authenticated after filling contact form

def home(req):
    # return HttpResponse("this is home")
    return render(req, "base.html")


def contact(req):
    if req.method == 'POST':
        form = contactForm(req.POST)
        if form.is_valid():
            # ! sending mails 
            
            mail_to_user = EmailMultiAlternatives(
                "Mail From Lazy coder",
                f"Thanks for Visiting our Blog and contacting us, Our team will approach you soon on your given email address or phone number.<br>Your responses are :-{form}",
                "bablu123890kumar@gmail.com",
                [f"{req.POST.get('email')}"],
            )
                                                  
            mail_to_lazycoder = EmailMultiAlternatives(
                f"{form.cleaned_data.get('name')} has Contacted us.",
                f"Some one wants to contact us<br>responses are<br>{form}",
                "bablu123890kumar@gmail.com",
                ["kunalverma.learn@gmail.com"],
            )
            
            mail_to_user.content_subtype = 'html'
            mail_to_lazycoder.content_subtype = 'html'
            
            # ! implemented multithreading to make response faster
            thread.sendMail(mail_to_user, mail_to_lazycoder).start()
            
            form.save()

            messages.info(req, f"Contact request recieved for{form.cleaned_data.get('name')}. Our team will contact to soon.")
            
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


def handle(req, s):
    return HttpResponse(f"This is {s} that you typed in url")
