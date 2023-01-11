from django.urls import path
from . import views

urlpatterns = [
    path("test", views.TestView.as_view()),
    # path("file", views.FileView.as_view()),
    path("format", views.FormatView.as_view()),
    path("files", views.FileViews.as_view()),
    path("main", views.PictureView.as_view()),
    # path("article", views.SearchViews.as_view()),
    # path("articles", views.SearchView.as_view()),

]
