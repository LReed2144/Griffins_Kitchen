from django.urls import path
from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("settings/", views.settings, name="settings"),
    path("upload", views.upload, name="upload"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("home_page", views.home_page, name="home_page"),
    path("all-recipes", views.all_recipes, name="all_recipes"),
    path("follow/", views.follow, name="follow"),
    path("follow/", views.follow, name="follow"),
    path("like_post", views.like_post, name="like_post"),
    path('profile/<str:pk>', views.profile, name='profile')
]