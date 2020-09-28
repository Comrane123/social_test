from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from .models import Post, Like
from accounts.models import Profile

from django.contrib.auth import get_user_model

User = get_user_model()


def like_unlike_post(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile.user)
        else:
            post_obj.liked.add(profile.user)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == "Like":
                like.value = "Unlike"
                like.save()

            else:
                like.value = "Like"
                like.save()
        else:
            like.value = "Like"

            post_obj.save()
            like.save()

    return redirect("home")


class PostList(SelectRelatedMixin, generic.ListView):
    model = Post
    select_related = ("user",)


class UserPosts(generic.ListView):
    model = Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_login = self.post_user.last_login
        context["last_login"] = last_login
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = Post
    select_related = ("user",)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get("username"))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ("message",)
    model = Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = Post
    select_related = ("user",)
    success_url = reverse_lazy("home")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)
