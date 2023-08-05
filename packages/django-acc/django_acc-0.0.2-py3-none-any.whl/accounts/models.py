from django.db import models
from django.contrib.auth.models import User

# Create your models here.

"""Extending the Django's User model"""
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200)
