from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    
    gen_choice = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    
    phone_number = PhoneNumberField(blank=True)
    date_of_birth = models.DateField(default=timezone.now)
    address = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=500, blank=True,default="")
    tagline = models.CharField(max_length=200, blank=True,default="")
    gender = models.CharField(choices=gen_choice, null=False, default='M', max_length=10)
    fb = models.URLField(max_length=100, null=True, blank=True,)
    insta = models.URLField(max_length=100, null=True, blank=True,)
    twitter = models.URLField(max_length=100, null=True, blank=True,)
    snap = models.URLField(max_length=100, null=True, blank=True,)
    github = models.URLField(max_length=100, null=True, blank=True,)
    website = models.URLField(max_length=100, null=True, blank=True,)
    linkedin = models.URLField(max_length=100, null=True, blank=True,)
    
    
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self ,*args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            new_img_size = (500,500)
            img.thumbnail(new_img_size)
            img.save(self.image.path)
            

# TODO : There might be some bug in prifle picture saving and deleting previous one, check it out
