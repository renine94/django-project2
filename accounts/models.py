from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('이메일 주소', unique=True)
    nickname = models.CharField('닉네임', max_length=30)
    phone_number = models.CharField('핸드폰번호', max_length=11, unique=True)
    confirm_code = models.CharField('임시코드', max_length=6)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone_number']


