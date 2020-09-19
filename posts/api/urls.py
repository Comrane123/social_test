from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import PostList, PostDetail, CommentList, CommentDetail

urlpatterns = [
    path("posts/", PostList.as_view()),
    path("posts/<int:pk>/", PostDetail.as_view()),
    path("comments/", CommentList.as_view()),
    path("comments/<int:pk>/", CommentDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
