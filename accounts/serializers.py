from rest_framework import serializers

from accounts.models import User


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'nickname', 'password', 'username', 'phone_number')