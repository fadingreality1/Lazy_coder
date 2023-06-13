from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, HttpResponseRedirect
from .models import Post, Comment
from django.contrib import messages
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required
from home.views import get_ip
from home.models import VUser
from django.urls import reverse
# Create your views here.

# TODO : add viewer incremet function before every route so that every ip is captured

# TODO : Likes and views to be added in to model along with comments

def home(req):
    posts = Post.objects.all().order_by('-date_posted')
    return render(req, "blog/home.html", {'posts':posts})

# TODO : viewers count is fucking me up

def post(req, slug):
    try:
        post = Post.objects.get(slug = slug)
        ip = get_ip(req)
        # Capturing any new viewer
        if not VUser.objects.filter(ip = ip).exists():
            VUser(ip = ip).save()
            
        # !comments handling
        comments = Comment.objects.filter(Q(post = post) & Q(parent = None)).order_by('-date_posted')
    except:
        messages.error(req, f"No such page exists for '{slug.replace('-', ' ')}'.")
        return redirect("home")
    # viewer = VUser(ip = ip)
    # # viewer.save()
    # post = Post.objects.get(slug = slug)
    # post.save()
    # post.viewers.add(viewer)
   
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
        parent_id = req.POST.get('parent_id')
        print(parent_id)
        if parent_id == "":
            comment = Comment(user = req.user, content = content, post = post, parent = None)
            messages.success(req, f"Comment Posted Successfully")
        else:
            parent = Comment.objects.get(id = parent_id)
            comment = Comment(user = req.user, content = content, post = post, parent = parent)
            messages.success(req, f"Reply to {parent.user.first_name}'s Comment Posted Successfully")
        comment.save()
        return redirect('post_detail', slug = slug)

    return redirect('home')
# TODO : add like and disike buttons to comments as well as post
# TODO : add delete button for comments for author of comment and author of post

@login_required(login_url='signin')
def like(req):
    post = Post.objects.filter(id = req.POST.get('post_id')).first()
    liked = Post.objects.filter(id = req.POST.get('post_id'), likers = req.user).exists()
    disliked = Post.objects.filter(id = req.POST.get('post_id'), dislikers = req.user).exists()
    if liked:
        post.likers.remove(req.user)
        post.save()
    else:
        post.likers.add(req.user)
        post.save()
        
    if disliked:
        post.dislikers.remove(req.user)
        post.save()
        
    return redirect('post_detail', slug = post.slug)



@login_required(login_url='signin')   
def dislike(req):
    post = Post.objects.filter(id = req.POST.get('post_id')).first()
    liked = Post.objects.filter(id = req.POST.get('post_id'), likers = req.user).exists()
    disliked = Post.objects.filter(id = req.POST.get('post_id'), dislikers = req.user).exists()
    if disliked:
        post.dislikers.remove(req.user)
        post.save()
    else:
        post.dislikers.add(req.user)
        post.save()
    
    if liked:
        post.likers.remove(req.user)
        post.save()
        
    return redirect('post_detail', slug = post.slug)
