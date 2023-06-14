from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from home.models import VUser
from PIL import Image


# TODO : Likes and views to be added in to model along with comments
# ? Category Model

class Category(models.Model):
    title = models.CharField(max_length=200, blank=False, unique=True)

    def __str__(self):
        return self.title

# ? To give defult value to categories
def uncategorized():
    return Category.objects.filter(title = 'Uncategorized')

class Post(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=250,null=True)
    content = RichTextField(blank=False, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='blog/default.jpg', upload_to='blog')
    slug = AutoSlugField(populate_from = 'title', unique=True, null=True, default=None, always_update = True,)
    # ! likes, dislikes, views, category
    viewers = models.ManyToManyField(VUser, related_name="viewers", blank=True)
    likers = models.ManyToManyField(User, related_name='liked', blank=True)
    dislikers = models.ManyToManyField(User, related_name='disliked', blank=True)
    categories = models.ManyToManyField(Category, related_name="category", default=uncategorized,blank=False)

    def __str__(self):
        return f'{self.title}'

    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    # ! parent comment
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='replies')

    def __str__(self):
        return f'{self.content[:200] } :: {self.parent}'




    