from django.urls import path
from . import views

urlpatterns = [
    path("test", views.TestView.as_view()),
    path("main", views.MainView.as_view()),
]
