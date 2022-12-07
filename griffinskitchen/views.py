from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth


from .models import Profile, Post, User, LikePost




def index(request):
    return render(request, "griffinskitchen/index.html")
 

@login_required
def home_page(request):
    return render(request, "griffinskitchen/home_page.html")

@login_required
def all_recipes(request):
    #get object of current login user
    user_object = User.objects.get(username=request.user.username)
    #get their profile
    user_profile = Profile.objects.get(user=user_object)

    posts=Post.objects.all()

    return render(request, "griffinskitchen/all_recipes.html",{'user_profile':user_profile, 'posts':posts})

   

def follow(request):
    return render(request, "griffinskitchen/follow.html")

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