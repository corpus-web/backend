from django.urls import path
from . import views

urlpatterns = [
    path("list", views.PrizeView.as_view()),
    path("lists", views.PrizeViews.as_view()),
    path("delete", views.DeleteView.as_view())
]
