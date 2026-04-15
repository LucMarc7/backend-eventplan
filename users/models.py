from django.db import models
from django.contrib.auth.models import  User
import uuid
# Create your models here.

class UserProfile(models.Model):
    profile_image = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField()
    country = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username