from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from django.db.models import DateTimeField
from django.db import models

# Create your models here.

# User model

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
    
# Exercise model

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


# Feedback model

class FeedbackManager(models.Manager):

    def create_feedback(self, user_id, feedback_type, content):
        feedback = self.create(user_id = user_id, feedback_type = feedback_type, content = content)
        feedback.save(using=self._db)
        return feedback

class Feedback(models.Model):

    user_id = models.IntegerField(null = False)
    feedback_id = models.AutoField(primary_key=True, auto_created=True)
    feedback_type = models.CharField(max_length=11)
    content = models.CharField(max_length=1000)
    state = models.BooleanField(default = False)

    on_delete = models.CASCADE

    objects = FeedbackManager()

# Routine model
    
class RoutineManager(models.Manager):

    def create_routine(self,user_id, exercises, name, description, logo):
        routine = self.model(
            name= name,
            user_id = user_id,
            exercises = exercises,
            description = description,
            logo = logo
        )
        routine.save(using=self.db)
        return routine


class Routine(models.Model):

    id = models.AutoField(primary_key=True, auto_created = True)
    name = models.CharField(unique=True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    exercises = ArrayField(models.IntegerField(null = False))
    description = ArrayField(models.CharField(null = False))
    logo = models.CharField(unique=True)

    objects = RoutineManager()

# History model
    
class HistoryManager(models.Manager):

    def create_history(self,user_id, action):
        history = self.model(
            user_id = user_id,
            action = action,
        )
        history.save(using=self.db)
        return history


class History(models.Model):

    id = models.AutoField(primary_key=True, auto_created = True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    action = models.CharField()
    date = DateTimeField(auto_now_add=True)

    objects = HistoryManager()