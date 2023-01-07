from django.urls import path
from . import views

urlpatterns = [
    path("main", views.PictureView.as_view()),
]
