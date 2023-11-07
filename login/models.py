from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    
    def create_user(self, username, password, email):
        user = self.model(
            username = username,
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password, email):
        user = self.create_user(
            username,
            password,
            email
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    todayLoginAttempts = models.IntegerField(default=0)
    lastLoginAttemptDate = models.DateTimeField(null=True, blank=True, auto_now=True)
    active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password", "email"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

class Exercise(models.Model):
    
    MUSCLE_GROUPS = [
        ("Pierna","LEGS"),
        ("Brazo","ARMS"),
        ("Abdomen","ABDOMINALS"),
        ("Pecho","CHEST"),
        ("Espalda","BACK"),
        ("Hombros","SHOULDERS")
    ]

    id = models.AutoField(primary_key=True, auto_created = True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(unique=True)
    level = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])
    group = models.CharField(blank=True, choices=MUSCLE_GROUPS)
    url = models.CharField(blank=True,unique=True)
    logo = models.CharField(blank=True,unique=True)

    def __str__(self):
        string = self.name + ' (' + str(self.id) + ')' 
        return string
