from django.shortcuts import render, redirect
from .models import Post, Comment, Category
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from home.views import get_ip
from home.models import VUser
from django.core.paginator import Paginator
from .forms import PostCreateForm
import os
from django.utils import timezone

def home(req):
    try: 
        ip = get_ip(req)
        viewer, _ = VUser.objects.get_or_create(ip = ip)
        viewer.last_seen = timezone.now()
        viewer.save()
        posts = Post.objects.all().order_by('-date_posted')
        p = Paginator(posts, 10)
        page_number = req.GET.get('page')
        data_showing = p.get_page(page_number)
        return render(req, "blog/home.html", {'posts':data_showing,})
    except Exception as e:
        messages.error(req, "Some error occured while fetching posts, contact Lazy Coder team.")
        return redirect("home")

def post(req, slug):
    try:
        post = Post.objects.get(slug = slug)
        ip = get_ip(req)
        viewer, _ = VUser.objects.get_or_create(ip = ip)
        viewer.last_seen = timezone.now()
        viewer.save()
        post.viewers.add(viewer)
        post.save()
        comments = Comment.objects.filter(Q(post = post) & Q(parent = None)).order_by('-date_posted')
        return render(req, "blog/post.html", {'post':post, 'comments': comments})
    except Exception as e:
        messages.error(req, f"No such page exists for '{slug.replace('-', ' ')}'.")
        return redirect("home")

@login_required(login_url='signin')
def createPost(req):
    try:
        if req.method == "POST":
            form = PostCreateForm(req.POST, req.FILES)
            choice_selected = [int(x) for x in req.POST.getlist('category')]
            if form.is_valid():
                post = form.save(commit = False)
                post.author = req.user
                post.save()
                for i in choice_selected[:3]:
                    post.categories.add(Category.objects.get(id = i))
                return redirect("post_detail", slug = post.slug)
            return render(req, "blog/create_post.html", {"form":form})
        form = PostCreateForm()
        return render(req, "blog/create_post.html", {"form":form})
    except:
        messages.error(req, "Some error occured while creating the post, Kindly contact Lazy Coder Team.")
        return redirect("home")

@login_required(login_url='signin')
def postComment(req, slug):
    try:
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
    except Exception:
        messages.error(req, "Some error occurred while posting comment. Kindly contact Lazy Coder Team.")
        return redirect("home")

@login_required(login_url='signin')
def like(req):
    try:
        post = Post.objects.filter(id = req.POST.get('post_id')).first()
        liked = Post.objects.filter(id = req.POST.get('post_id'), likers = req.user).exists()
        disliked = Post.objects.filter(id = req.POST.get('post_id'), dislikers = req.user).exists()
        if liked:
            post.likers.remove(req.user)
        else:
            post.likers.add(req.user)
        if disliked:
            post.dislikers.remove(req.user)
        return redirect('post_detail', slug = post.slug)
    except Exception as e:
        messages.error(req, "Some error occurred while liking the post. Kindly contact Lazy Coder Team.")
        return redirect("home")

@login_required(login_url='signin')   
def dislike(req):
    try:
        post = Post.objects.filter(id = req.POST.get('post_id')).first()
        liked = Post.objects.filter(id = req.POST.get('post_id'), likers = req.user).exists()
        disliked = Post.objects.filter(id = req.POST.get('post_id'), dislikers = req.user).exists()
        if disliked:
            post.dislikers.remove(req.user)
        else:
            post.dislikers.add(req.user)
        if liked:
            post.likers.remove(req.user)
        return redirect('post_detail', slug = post.slug)
    except Exception as e:
        messages.error(req, "Some error occurred while disliking the post. Kindly contact Lazy Coder Team.")
        return redirect("home")

def categoryPost(req, category, username = None):
    try:
        cat = Category.objects.get(title = category)
        cat_id = cat.id
        all_posts = Post.objects.filter(categories = cat_id).order_by("-date_posted")
        c = True
        cu = False
        user = None
        if username != None:
            user = User.objects.filter(username=username).first()
            uid = user.id
            all_posts = all_posts.filter(author = uid).order_by("-date_posted")
            c = False
            cu = True
        p = Paginator(all_posts, 10)
        page_number = req.GET.get('page')
        data_showing = p.get_page(page_number)
        return render(req, "blog/category.html", {"posts": data_showing, "catname": category, "uname":user, "c": c, 'cu': cu})
    except Exception as e:
        messages.error(req, "No such category exists")
        return redirect("home")

@login_required(login_url="signin")
def update(req, slug):
    try:
        if req.method == "POST":
            prev_post = Post.objects.get(slug = slug)
            if prev_post.author != req.user:
                messages.warning(req, "Not your Post nigga.")
                return redirect("home")
            old_image = ''
            if os.path.isfile(prev_post.image.path):
                old_image = prev_post.image.path
            
            form = PostCreateForm(req.POST, req.FILES, instance=prev_post)
            if form.is_valid():
                for i in prev_post.categories.all():
                    prev_post.categories.remove(i)
                Updated_post = form.save()
                choice_selected = [int(x) for x in req.POST.getlist('category')]
                for i in choice_selected[:3]:
                    Updated_post.categories.add(Category.objects.get(id = i))
                if os.path.exists(old_image) and req.POST.get('image') != None :
                    os.remove(old_image)
                messages.success(req, "Post has been updated successfully.")
                return redirect("post_detail", slug = Updated_post.slug)
            else:
                return render(req, "blog/update_post.html", {'form':form, 'slug':prev_post.slug})
        post = Post.objects.get(slug = slug)
        if post.author != req.user:
            messages.warning(req, "Not your Post nigga.")
            return redirect("home")
        prev_choices = post.categories.all()
        form = PostCreateForm(instance=post, initial={'category': prev_choices})
        return render(req, "blog/update_post.html", {'form': form, 'slug':post.slug})
    except Exception as e:
        messages.error(req, "No Such page exists")
        return redirect("home")

@login_required(login_url="signin")
def delete(req):
    try:
        post = Post.objects.filter(id = req.POST.get("post_id")).first()
        if post.author != req.user:
            messages.warning(req, "Not your Post nigga.")
            return redirect("home")
        old_image = post.image.path
        post.delete()
        os.remove(old_image)
        messages.success(req, "Post Deleted Successfully.")
        return redirect("home")
    except Exception as e:
        messages.error(req, "Some error occured While deleting the post, contact Lazy Coder team")
        return redirect("home")
    
@login_required(login_url="signin")
def deleteComment(req, id, slug):
    try:
        comment = Comment.objects.get(id = id)
        if comment.user == req.user or comment.post.author == req.user and comment.post.slug == slug:
            comment.delete()
            messages.success(req, "Comment removed successfully.")
            return redirect("post_detail", slug = slug)
        messages.warning(req, "Not your territory nigga.")
        return redirect("post_detail", slug = slug)
    except Exception as e:
        messages.error(req, "Some internal error occured While deletion of comment, contact Lazy Coder Team")
        return redirect("home")
    
def userPost(req, username):
    try:
        user = User.objects.get(username = username)
        all_posts = Post.objects.filter(author = user).order_by("-date_posted")
        p = Paginator(all_posts, 10)
        page_number = req.GET.get('page')
        data_showing = p.get_page(page_number)
        return render(req, "blog/category.html", {'posts':data_showing, 'uname':user, "u":True,})
    except Exception as e:
        messages.error(req, "Some error ocuured while filtering posts by Authors, That author might not exists.")
        return redirect("home")
    
def categories(req):
    categories = Category.objects.all().order_by('title')
    n = categories.count()
    c1 = categories[:n//2]
    c2 = categories[n//2:]
    return render(req, "blog/categories.html", {'categories1': c1, 'categories2':c2})