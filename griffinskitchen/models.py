from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime


User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    about = models.TextField(blank=True)


    # Relationships
    # OneToOne: 
    # ManyToOne: ForeignKey
    # ManyToMany

    # Reverse Relatinoships
    # user_posts = Post.objects.get(user=user)
    # posts = user.posts.all()

    # followers = models.ManyToManyField(User, related_name="get_followed_profiles")




    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images')
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    likes = models.IntegerField(default=0)
    #comments =

    # Relationships



   
    def __str__(self):
        return self.user


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username



class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user