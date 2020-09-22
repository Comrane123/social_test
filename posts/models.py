from django.urls import reverse
from django.db import models

import misaka

from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):

    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    likes = models.ManyToManyField(User, related_name="post_like")

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse(
            "posts:single", kwargs={"username": self.user.username, "pk": self.pk}
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]
