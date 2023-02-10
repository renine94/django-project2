from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField('이메일 주소', unique=True)
    username = models.CharField('이름', max_length=30, validators=[UnicodeUsernameValidator()])
    nickname = models.CharField('닉네임', max_length=30)
    phone_number = models.CharField('핸드폰번호', max_length=11, unique=True)
    confirm_code = models.CharField('임시코드', max_length=6)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone_number']


class PhoneAuthentication(models.Model):
    phone_number = models.CharField(max_length=11)
    confirm_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'accounts_phone_authentication'
        unique_together = (('phone_number', 'confirm_code'),)
