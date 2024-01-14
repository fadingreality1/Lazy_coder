from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from home.models import VUser
from PIL import Image
import os
import base64


class Category(models.Model):
    title = models.CharField(max_length=200, blank=False, unique=True)
    def __str__(self):
        return self.title

def uncategorized():
    return Category.objects.filter(title = 'Uncategorized')

class Post(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=250,null=True)
    content = RichTextField(blank=False, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # image = models.ImageField(upload_to='blog')
    proxyimage = models.ImageField(upload_to='blog', blank=True, default=None)
    image = models.TextField(db_column='image', blank=True, null=True)
    
    slug = AutoSlugField(populate_from = 'title', unique=True, null=True, default=None, always_update = True,)
    viewers = models.ManyToManyField(VUser, related_name="viewers", blank=True)
    likers = models.ManyToManyField(User, related_name='liked', blank=True)
    dislikers = models.ManyToManyField(User, related_name='disliked', blank=True)
    categories = models.ManyToManyField(Category, related_name="category", default=uncategorized,blank=False)

    def __str__(self):
        return f'{self.title}'
    
    def save(self ,*args, **kwargs):
        if self.proxyimage != '':
            super(Post, self).save(*args, **kwargs)
            old_path = self.proxyimage.path
            img = Image.open(self.proxyimage.path)
            if img.height > 1000 or img.width > 1000:
                new_img_size = (1000, 1000)
                img.thumbnail(new_img_size)
                img.save(self.proxyimage.path)
            img.close()
            with open(self.proxyimage.path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
                self.image = image_data
                self.proxyimage = None
            os.remove(old_path)
            
        super(Post, self).save(*args, **kwargs)
        
        
        

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='replies')

    def __str__(self):
        return f'{self.content[:200] } :: {self.parent}'




    