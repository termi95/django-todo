from django.urls import path
from . import views

urlpatterns = [
    path("home", views.main, name="main"),
    path("todomanager", views.todomanager, name="todomanager"),
    path("task-list", views.getTaskList, name="getTaskList"),
    path("add", views.add, name="add"),
    path("delete/<int:task_id>", views.delete, name="delete"),
    path('edit/<int:task_id>/', views.edit, name='edit'),
    path('task/<int:task_id>/', views.getTask, name='getTask'),
    path('done/<int:task_id>/', views.done, name='done'),
]