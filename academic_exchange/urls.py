from django.urls import path
from . import views

urlpatterns = [
    path("title", views.ListView.as_view()),
    path("content", views.ContentView.as_view()),
    path("main", views.PictureView.as_view()),
    path("delete", views.DeleteView.as_view())
]
