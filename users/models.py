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
    profile_description = models.CharField(max_length=400, blank=True,default="")
    gender = models.CharField(choices=gen_choice, null=False, default='M', max_length=1)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self ,*args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            new_img_size = (500,500)
            img.thumbnail(new_img_size)
            img.save(self.image.path)
            

# TODO : There might be some bug in prifle icture saving and deleting previous one, check it out
