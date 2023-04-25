from django.urls import path
from . import views

urlpatterns = [
    path("title", views.MessageTitleView.as_view()),
    path("context", views.MessageContextView.as_view()),
    path("delete", views.DeleteView.as_view())
]
