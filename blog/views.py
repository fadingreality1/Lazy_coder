from django.shortcuts import render, HttpResponse, redirect
from .models import Post, Comment
from django.contrib import messages
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required
# Create your views here.

# TODO : Likes and views to be added in to model along with comments

def home(req):
    posts = Post.objects.all().order_by('-date_posted')
    return render(req, "blog/home.html", {'posts':posts})

def post(req, slug):
    try:
        post = Post.objects.get(slug = slug)
        post.views = F('views') + 1
        post.save()
        comments = Comment.objects.filter(Q(post = post) & Q(parent = None)).order_by('-date_posted')
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
