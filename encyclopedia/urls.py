from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.entry, name = "entry"),
    path("create", views.create, name="create"),
    path("random", views.random_page, name="random")
]
