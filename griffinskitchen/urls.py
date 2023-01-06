from django.urls import path
from . import views 
# from . views import AddCommentView

urlpatterns = [
    path("", views.index, name="index"),
    path("settings/", views.settings, name="settings"),
    path("all_recipes/upload", views.upload, name="upload"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("all_recipes/", views.all_recipes, name="all_recipes"),
    path("follow", views.follow, name="follow"),
    path("like_post", views.like_post, name="like_post"),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('search', views.search, name="search")
]