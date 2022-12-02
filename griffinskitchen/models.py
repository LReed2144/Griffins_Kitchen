from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = pass
    profile_img = models.ImageField()
    about = pass
    followers = models.ManyToManyField(User, related_name="get_followed_profiles")

 