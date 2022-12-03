from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "griffinskitchen/index.html")

def home_page(request):
    return render(request, "griffinskitchen/home_page.html")

def all_recipes(request):
    return render(request, "griffinskitchen/all_recipes.html")

def follow(request):
    return render(request, "griffinskitchen/follow.html")


@login_required
def settings(request):
    return render(request, "griffinskitchen/settings.html")


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
            # Profile(user=user).save()
        except IntegrityError:
            return render(request, "griffinskitchen/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "griffinskitchen/register.html")