from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from posts.api.views import PostListAPIView, PostDetailAPIView, LikeListAPIView

urlpatterns = [
    path("posts/", PostListAPIView.as_view()),
    path("posts/<int:pk>/", PostDetailAPIView.as_view()),
    path("likes/", LikeListAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
