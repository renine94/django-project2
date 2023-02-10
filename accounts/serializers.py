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
        self.validated_data.pop('password2')
        return super().save(**kwargs)

    def validate(self, attrs):
        p1 = attrs['password']
        p2 = attrs['password2']
        if p1 != p2:
            raise serializers.ValidationError('Password is must same!')
        return attrs





