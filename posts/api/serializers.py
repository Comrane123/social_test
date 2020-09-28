from rest_framework import serializers

from posts.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "user", "created_at", "message"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["post", "user", "value", "created", "updated"]
