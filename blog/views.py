from django.shortcuts import render, HttpResponse, redirect
from .models import Post, Comment, Category
from django.contrib import messages
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required
from home.views import get_ip
from home.models import VUser
from django.core.paginator import Paginator
from .forms import PostCreateForm
import os
from Lazy_coder.settings import MEDIA_ROOT, MEDIA_URL
# Create your views here.

# TODO : add viewer incremet function before every route so that every ip is captured

# TODO : Likes and views to be added in to model along with comments

def home(req):
    posts = Post.objects.all().order_by('-date_posted')
    p = Paginator(posts, 10)
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
    except Exception as e:
        messages.error(req, f"No such page exists for '{slug.replace('-', ' ')}'.")
        return redirect("home")
    return render(req, "blog/post.html", {'post':post, 'comments': comments})

@login_required(login_url='signin')
def createPost(req):
    if req.method == "POST":
        form = PostCreateForm(req.POST, req.FILES)
        choice_selected = [int(x) for x in req.POST.getlist('category')]
        if form.is_valid():
            post = form.save(commit = False)
            post.author = req.user
            # ? saving the post first is req before we use "add" fucntion because it works on "id" and without saving, we won't have a "id".
            
            post.save()
            # ? this is the method by which we can add many to many fields in our posts.
            
            for i in choice_selected[:3]:
                post.categories.add(Category.objects.get(id = i))
                
            # ? add function automatically saves the Post object and we don't need to call save() method again
            
            return redirect("post_detail", slug = post.slug)
        else:
            return render(req, "blog/create_post.html", {"form":form})
        
    form = PostCreateForm()
    return render(req, "blog/create_post.html", {"form":form})
        


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
        # ? We don't need to call save method again because add and remove method does it themselves.
    else:
        post.likers.add(req.user)
        # ? We don't need to call save method again because add and remove method does it themselves.
        
    if disliked:
        post.dislikers.remove(req.user)
        # ? We don't need to call save method again because add and remove method does it themselves.
        
    return redirect('post_detail', slug = post.slug)



@login_required(login_url='signin')   
def dislike(req):
    post = Post.objects.filter(id = req.POST.get('post_id')).first()
    liked = Post.objects.filter(id = req.POST.get('post_id'), likers = req.user).exists()
    disliked = Post.objects.filter(id = req.POST.get('post_id'), dislikers = req.user).exists()
    if disliked:
        post.dislikers.remove(req.user)
        # ? We don't need to call save method again because add and remove method does it themselves.
    else:
        post.dislikers.add(req.user)
        # ? We don't need to call save method again because add and remove method does it themselves.
    
    if liked:
        post.likers.remove(req.user)
        # ? We don't need to call save method again because add and remove method does it themselves.
        
    return redirect('post_detail', slug = post.slug)

def category(req, category):
    # ! make some changes 
    try:
        cat = Category.objects.get(title = category)
        cat_id = cat.id
        all_posts = Post.objects.filter(categories = cat_id)
        p = Paginator(all_posts, 10)
        page_number = req.GET.get('page')
        data_showing = p.get_page(page_number)
        return render(req, "blog/category.html", {"posts": data_showing, "category": category,})
    except:
        messages.error(req, "No such category exists")
        return redirect("home")
    
    
@login_required(login_url="signin")
def update(req, slug):
    # try:
        if req.method == "POST":
            prev_post = Post.objects.get(slug = slug)
            old_image = (f'{MEDIA_ROOT}'+ f'{prev_post.image.url}').replace("\\", "/").replace('media/media/', 'media/')
            # ! if someone tries to access other people's post
            if prev_post.author != req.user:
                messages.warning(req, "Not your Post nigga.")
                return redirect("home")
            
            form = PostCreateForm(req.POST, req.FILES, instance=prev_post)
            

            if form.is_valid():
                # ! Removing previously selected categories
                # prev_choices = prev_post.categories.all
                # ! it is iterable but above line is not
                
                for i in prev_post.categories.all():
                    prev_post.categories.remove(i)
                
                # ? Adding newly selected fields
                Updated_post = form.save()
                choice_selected = [int(x) for x in req.POST.getlist('category')]
                
                for i in choice_selected[:3]:
                    Updated_post.categories.add(Category.objects.get(id = i))
                
                if os.path.exists(old_image) and req.POST.get('image') == None and old_image != f'{MEDIA_ROOT}'+'\\profile_pics\\default.png' :
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

    # except:
        messages.error(req, "No Such page exists")
        return redirect("home")


@login_required(login_url="signin")
def delete(req):
    try:
        post = Post.objects.filter(id = req.POST.get("post_id")).first()
        old_image = (f'{MEDIA_ROOT}'+ f'{post.image.url}').replace("\\", "/").replace('media/media/', 'media/')
        if post.author != req.user:
            return redirect("home")
        post.delete()
        os.remove(old_image)
        messages.success(req, "Post Deleted Successfully.")
        return redirect("home")
    except:
        messages.error(req, "Some error occured")
        return redirect("home")