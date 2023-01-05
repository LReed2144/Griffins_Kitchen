from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from itertools import chain
import random
from django.views.generic.edit import CreateView

from .models import Profile, Post, User, LikePost, FollowersCount, Comments




def index(request):
    return render(request, "griffinskitchen/index.html")
 

@login_required
def home_page(request):
    return render(request, "griffinskitchen/home_page.html")

@login_required
def all_recipes(request,):
    #get object of current login user
    user_object = User.objects.get(username=request.user.username)
    #get their profile
    user_profile = Profile.objects.get(user=user_object)
   

    posts=Post.objects.all()

      # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    # already following
    user_following = FollowersCount.objects.filter(follower=request.user.username)

    #get list of already following
    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    #not already following
    # looping through all users not following
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    # remove self from the list
    current_user = User.objects.filter(username=request.user.username)
    # users that are left and randomize
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    # create lists
    username_profile = []
    username_profile_list = []

    #get ids of left over users
    for users in final_suggestions_list:
        username_profile.append(users.id)

    # add ids into a profile list
    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, "griffinskitchen/all_recipes.html", {'user_profile':user_profile, 'posts':posts, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})



@login_required
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        description = request.POST['description']
        ingredients = request.POST['ingredients']
        instructions = request.POST['instructions']

        new_post = Post.objects.create(user=user, image=image, description=description, ingredients=ingredients, instructions=instructions)
        new_post.save()
        return redirect('all_recipes')
    else:
        return redirect('all_recipes')

@login_required
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.likes = post.likes+1
        post.save()
        return redirect('all_recipes')
    else:
        like_filter.delete()
        post.likes = post.likes-1
        post.save()
        return redirect('all_recipes')

@login_required
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'griffinskitchen/home_page.html', context)
    



@login_required
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
            # return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('griffinskitchen/all_recipes')


@login_required
def settings(request):
    # currently getting the object 'user' from class Profile
    user_profile=Profile.objects.get(user=request.user)
        
    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profile_img
            about = request.POST['about']
           

            user_profile.profile_img = image
            user_profile.about = about
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            about = request.POST['about']
          

            user_profile.profile_img = image
            user_profile.about = about
            user_profile.save()
        
        return redirect('settings')

    return render(request, 'griffinskitchen/settings.html', {'user_profile': user_profile})


def search(request):
    #get user and user image
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        #returns any user with letters in the name from the database
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []
        
        #get user ids
        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'griffinskitchen/search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})
  

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home_page"))
        else:
            return render(request, "griffinskitchen/login.html", {
                "message": "Invalid username and/or password."
            })
    else:   
        return render(request, "griffinskitchen/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

 # password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "griffinskitchen/register.html", {
                "message": "Passwords must match."
            })

#  create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            #create a Profile object for the new user
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()

            # Profile(user=user).save()
        except IntegrityError:
            return render(request, "griffinskitchen/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home_page"))
    else:
        return render(request, "griffinskitchen/register.html")