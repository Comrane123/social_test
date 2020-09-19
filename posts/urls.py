from django.conf.urls import url
from django.urls import path

from .views import PostList, CreatePost, UserPosts, PostDetail, DeletePost

app_name = "posts"

urlpatterns = [
    url(r"new/$", CreatePost.as_view(), name="create"),
    url(r"by/(?P<username>[-\w]+)/$", UserPosts.as_view(), name="for_user"),
    url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$", PostDetail.as_view(), name="single"),
    url(r"delete/(?P<pk>\d+)/$", DeletePost.as_view(), name="delete"),
]
