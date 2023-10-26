from django.contrib.auth import get_user_model
from rest_framework import serializers

from account.utils import send_activation_code

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6 , required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')


    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password2')

        if p1 != p2:
            return serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code(user.email, user.activation_code)
        return user



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=6)
    password2 = serializers.CharField(required=True, min_length=6)

    def validate_password(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password2')

        if p1 != p2:
            return serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_new_password(self,validated_data):
        user = User.objects.get_password()
