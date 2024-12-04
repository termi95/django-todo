from django.urls import path
from . import views

urlpatterns = [
    path("home", views.main, name="main"),
    path("test", views.todomanager, name="todomanager"),
    path("add", views.add, name="add")
]