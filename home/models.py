from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


# Create your models here.

# ?Model for contact us page

class Contact(models.Model):
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=254, null=False)
    website = models.URLField(max_length=200, null=True, default=None)
    message = models.TextField(max_length=500, null=False)
    phone = PhoneNumberField(blank = True)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f'{self.name}---{self.email}'


# ! To get Total no of unique viewer on our site
class VUser(models.Model):
    ip = models.CharField(max_length=100,unique=True)
    arrived_first = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"user is {self.ip}"
