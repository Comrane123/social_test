from django.urls import reverse
from django.db import models

import misaka
from accounts.models import Profile

from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    liked = models.ManyToManyField(User, related_name="likes", blank=True)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.liked.all().count()

    def get_absolute_url(self):
        return reverse(
            "posts:single", kwargs={"username": self.user.username, "pk": self.pk}
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]


LIKE_CHOISES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, related_name='requirement_post_likes', on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOISES, max_length=8)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"
