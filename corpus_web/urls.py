from django.urls import path, include, re_path
from django.views.static import serve
from corpus_web import settings

# from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # path("api/docs/", include_docs_urls(title="corpus_web")),
    path("api/user/", include("user.urls")),
    path("api/home/", include("home.urls")),
    path("api/course/", include("course_construction.urls")),
    path("api/team/", include("team_style.urls")),
    path("api/academic/", include("academic_exchange.urls")),
    path("api/corpus/", include("corpus_content.urls")),
    path("api/message/", include("message.urls")),
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}, name='media'),
]
