from django.shortcuts import render, HttpResponse, redirect
from .models import Post, Comment
from django.contrib import messages
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required
from home.views import get_ip
from home.models import VUser
from django.core.paginator import Paginator
# Create your views here.

# TODO : add viewer incremet function before every route so that every ip is captured

# TODO : Likes and views to be added in to model along with comments

def home(req):
    posts = Post.objects.all().order_by('-date_posted')
    p = Paginator(posts, 1)
    page_number = req.GET.get('page')
    data_showing = p.get_page(page_number)
    return render(req, "blog/home.html", {'posts':data_showing,})

def post(req, slug):
    try:
        post = Post.objects.get(slug = slug)
        ip = get_ip(req)
        
        # if VUser.objects.filter(ip = ip).exists():
        #     ouser = VUser.objects.get(ip = ip)
        #     post.viewers.add(ouser)
        #     post.save()
        # else:
        #     nuser = VUser(ip = ip)
        #     nuser.save()
        #     post.viewers.add(nuser)
        #     post.save()
        # ! better method to get the user and if it doesn't exists, create it.
        
        # ? get_or_create() returns a tuple, one object and one is flag whether object created or already existed in the DB.
        viewer, _ = VUser.objects.get_or_create(ip = ip)
        post.viewers.add(viewer)
        post.save()
            
        # !comments handling
        comments = Comment.objects.filter(Q(post = post) & Q(parent = None)).order_by('-date_posted')
    except:
        messages.error(req, f"No such page exists for '{slug.replace('-', ' ')}'.")
        return redirect("home")
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
