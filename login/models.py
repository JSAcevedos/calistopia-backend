from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class User(AbstractBaseUser):

    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    todayLoginAttempts = models.IntegerField(default=0)
    lastLoginAttemptDate = models.DateTimeField(null=True, blank=True, auto_now=True)
    active = models.BooleanField(default=False)

    USERNAME_FIELD = "id"

