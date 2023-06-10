from django.shortcuts import render, HttpResponse, redirect
from .models import Post, Comment
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

# TODO : Likes and views to be added in to model along with comments

def home(req):
    posts = Post.objects.all().order_by('-date_posted')
    return render(req, "blog/home.html", {'posts':posts})

def post(req, slug):
    try:
        post = Post.objects.get(slug = slug)
        comments = Comment.objects.filter(post = post).order_by('-date_posted')
    except:
        messages.error(req, f"No such page exists for '{slug.replace('-', ' ')}'.")
        return redirect("home")
    
    # return render(req, "blog/post.html", {'post':post,})
    return render(req, "blog/post.html", {'post':post, 'comments': comments})

def createPost(req):
    return HttpResponse("create post called")


# TODO : apply pagination to comments and main blog page
# TODO : create profile page and update and delete route 


@login_required(login_url='signin')
def postComment(req, slug):
    if req.method == "POST":
        post = Post.objects.get(slug = slug)
        content = req.POST.get('comment')
        comment = Comment(user = req.user, content = content, post = post, parent = None)
        comment.save()
        messages.success(req, "Comment Posted Successfully")
        return redirect('post_detail', slug = slug)

    return redirect('home')