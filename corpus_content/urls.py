from django.urls import path
from . import views

urlpatterns = [
    path("file", views.FileView.as_view()),
    path("format", views.FormatView.as_view()),
    path("files", views.FileViews.as_view()),
    path("main", views.PictureView.as_view()),
    path("category", views.CategoryView.as_view()),
    path("delete/<int:nid>", views.DeleteView.as_view())
]
