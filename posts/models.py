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

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_total_likes(self):
        return self.likes.users.count()

    def get_absolute_url(self):
        return reverse(
            "posts:single", kwargs={"username": self.user.username, "pk": self.pk}
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]


class Like(models.Model):
    """ Like model for posts """

    post = models.OneToOneField(Post, related_name="likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="requirement_post_likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.post)[:30]
