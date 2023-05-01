from django.urls import path
from . import views

urlpatterns = [
    path("main", views.MainView.as_view()),
    path("delete", views.DeleteView.as_view())
]
