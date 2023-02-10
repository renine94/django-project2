from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from accounts.models import User


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    phone_number = serializers.CharField(style={'input_type': 'number'})

    class Meta:
        model = User
        fields = ('email', 'nickname', 'password', 'password2', 'username', 'phone_number')

    def save(self, **kwargs):
        """저장 전 비밀번호 암호화하고 password2 필드 제거"""
        hashed_password = make_password(self.validated_data['password'])

        self.validated_data.pop('password2')
        self.validated_data.update({'password': hashed_password})
        return super().save(**kwargs)

    def validate(self, attrs):
        p1 = attrs['password']
        p2 = attrs['password2']
        if p1 != p2:
            raise serializers.ValidationError('Password is must same!')
        return attrs


class MyTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)
