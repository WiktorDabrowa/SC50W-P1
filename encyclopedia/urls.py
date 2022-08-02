from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/random", views.random_page, name="random"),
    path("wiki/<str:entry_name>", views.entry, name = "entry"),
    path("create", views.create, name="create"),
    path("search", views.search, name="search"),
    path("wiki/<str:entry_name>/edit", views.edit, name="edit")
]
