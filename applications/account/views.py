from django.shortcuts import render
from rest_framework.generics import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager
from applications.account.serializers import RegisterSerializer



User = get_user_model()


class UserRegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
