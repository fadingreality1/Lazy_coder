from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField
import os
import base64


User._meta.get_field('email')._unique = True

class Profile(models.Model):
    gen_choice = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='profile_pics/', blank=True, null= True, default=None)
    
    proxyimage = models.ImageField(upload_to='profile_pics/', blank=True, default=None)
    
    image = models.TextField(db_column='image', blank=True, null=True)
    
    
    phone_number = PhoneNumberField(blank=True, null=True)
    date_of_birth = models.DateField(default=timezone.now, blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=500, blank=True,default="", null=True)
    tagline = models.CharField(max_length=200, blank=True,default="", null=True)
    gender = models.CharField(choices=gen_choice, null=False, default='M', max_length=10)
    fb = models.URLField(max_length=100, null=True, blank=True,)
    insta = models.URLField(max_length=100, null=True, blank=True,)
    twitter = models.URLField(max_length=100, null=True, blank=True,)
    snap = models.URLField(max_length=100, null=True, blank=True,)
    github = models.URLField(max_length=100, null=True, blank=True,)
    website = models.URLField(max_length=100, null=True, blank=True,)
    linkedin = models.URLField(max_length=100, null=True, blank=True,)
    
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self ,*args, **kwargs):
        if self.proxyimage:
            super(Profile, self).save(*args, **kwargs)
            old_path = self.proxyimage.path
            img = Image.open(self.proxyimage.path)
            if img.height > 500 or img.width > 500:
                new_img_size = (500, 500)
                img.thumbnail(new_img_size)
                img.save(self.proxyimage.path)
            img.close()
            with open(self.proxyimage.path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
                self.image = image_data
                self.proxyimage = None
            os.remove(old_path)
        super(Profile, self).save(*args, **kwargs)
