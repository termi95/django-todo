from django.urls import path
from . import views

urlpatterns = [
    path("home", views.main, name="main"),
    path("test", views.todomanager, name="todomanager"),
    path("task-list", views.getTaskList, name="getTaskList"),
    path("add", views.add, name="add"),
    path("delete/<int:task_id>", views.delete, name="delete"),
]