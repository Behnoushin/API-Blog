from django.db import models
from django.contrib.auth.models import AbstractUser
from utility.models import BaseModel

##################################################################################
#                           CustomUser Model                                     #
##################################################################################

class CustomUser(AbstractUser):
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    groups = models.ManyToManyField('auth.Group',related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_permissions_set', blank=True)
    
    def __str__(self):
        return self.username

##################################################################################
#                           UserProfile Model                                    #
##################################################################################

class UserProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"