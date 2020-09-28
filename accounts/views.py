import jwt

from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
from django.urls import reverse_lazy

from django.views.generic import CreateView
from rest_framework.generics import GenericAPIView

from . import forms
from .serializers import UserSerializer, LoginSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


class RegisterAPIView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get("username", "")
        password = data.get("password", "")
        user = auth.authenticate(username=username, password=password)

        if user:
            auth_token = jwt.encode(
                {"username": user.username}, settings.JWT_SECRET_KEY
            )

            serializer = UserSerializer(user)

            data = {"user": serializer.data, "token": auth_token}

            return Response(data, status=status.HTTP_200_OK)

            # SEND RES
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class LastLoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def get_serializer_context(self):
        context = super(LastLoginAPIView, self).get_serializer_context()
        context.update({
            "last_login": User.last_login
        })
        return context
