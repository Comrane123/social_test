from django.urls import path

from .views import CreatePost, UserPosts, PostDetail, DeletePost, LikeView

app_name = "posts"

urlpatterns = [
    path("new/", CreatePost.as_view(), name="create"),
    path("by/<str:username>/", UserPosts.as_view(), name="for_user"),
    path("by/<str:username>/<int:pk>/", PostDetail.as_view(), name="single"),
    path("delete/<int:pk>/", DeletePost.as_view(), name="delete"),
    path('like/<int:pk>', LikeView, name="like-post"),
]
