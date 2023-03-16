from django.urls import path
from . import views

urlpatterns = [
    path("login", views.LoginView.as_view()),
    path("create", views.UserCreateView.as_view()),
    path("change", views.PasswordChangeView.as_view()),
    path("cas", views.CasLoginView.as_view()),
]
