from django.urls import path
from .views import RegisterAPIView, LoginAPIView, RegisterView
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("api/register", RegisterAPIView.as_view()),
    path("api/login", LoginAPIView.as_view()),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", RegisterView.as_view(), name="signup"),
]
