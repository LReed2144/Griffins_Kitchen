from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    about = models.TextField(blank=True)
    # followers = models.ManyToManyField(User, related_name="get_followed_profiles")

    def __str__(self):
        return self.user.username

    