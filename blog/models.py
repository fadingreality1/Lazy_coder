from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from autoslug import AutoSlugField

# TODO : Likes and views to be added in to model along with comments

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250,null=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='blog/default.jpg', upload_to='blog')
    slug = AutoSlugField(populate_from = 'title', unique=True, null=True, default=None, always_update = True,)
    
    def __str__(self):
        return f'{self.title } by {self.author}'
    
    # def get_absolute_url(self):
    #     return reverse("post_detail", kwargs={"pk": self.pk})
    