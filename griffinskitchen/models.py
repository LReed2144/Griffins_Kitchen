from django.db import models
from django.contrib.auth import get_user_model



User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    about = models.TextField(blank=True)
    # followers = models.ManyToManyField(User, related_name="get_followed_profiles")

    def __str__(self):
        return self.user.username

    