from django.urls import path
from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.find , name="wiki"),
    path("search", views.search , name="search"),
    path("new", views.create , name="new"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("create", views.create_wiki, name="createwiki"),
    path("random", views.rand, name="random")
    
]
