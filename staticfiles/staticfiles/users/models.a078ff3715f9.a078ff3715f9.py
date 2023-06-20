from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField

User._meta.get_field('email')._unique = True

class Profile(models.Model):
    gen_choice = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', blank=True, null= True, default=None)
    phone_number = PhoneNumberField(blank=True, null=True)
    date_of_birth = models.DateField(default=timezone.now, blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=500, blank=True,default="")
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
        super(Profile, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 500 or img.width > 500:
                new_img_size = (500,500)
                img.thumbnail(new_img_size)
                img.save(self.image.path)
