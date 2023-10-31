from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from account.utils import send_activation_code, send_recovery_code

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



class ChangePasswordSerializers(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    new_password_confirm = serializers.CharField(required=True, min_length=6)

    def validate_old_password(self, password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(password):
            raise serializers.ValidationError('Пароль не совпадает с текущим')
        return user




    def validate(self, attrs):
        p1 = attrs.get('new_password')
        p2 = attrs.pop('new_password_confirm')
        old_password = attrs.get('old_password')
        request = self.context.get('request')
        user = request.user

        if user.check_password(p1):
            raise serializers.ValidationError('Новый пароль не должен совпадать с текущим')

        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs


    def set_new_password(self):
        request = self.context.get('request')
        user = request.user
        password = self._validated_data.get('new_password')
        user.set_password(password)
        user.save()


class PasswordRecoverySerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)

    def validate_email(self, email):
        user = User.objects.get(email=email)
        user.create_recovery_code()
        send_recovery_code(user.email, user.recovery_code)
        user.save()

        

class PasswordRecoverySetSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=60)
    new_password = serializers.CharField(min_length=6, required=True, write_only=True)
    new_password_confirm = serializers.CharField(min_length=6, required=True, write_only=True)

    def validate(self, attrs):
        p1 = attrs.get('new_password')
        p2 = attrs.get('new_password_confirm')

        if p1 != p2:
            raise serializers.ValidationError('Пароли совпадают')
        return attrs

    def validate_code(self, code):
        recovery_code = User.objects.get(recovery_code=code)
        if recovery_code == code:
            raise serializers.ValidationError('Код не верный')
        return code

    def set_new_password(self):
        code = self._validated_data.get('code')
        password = self._validated_data.get('new_password')
        user = User.objects.get(recovery_code=code)
        user.set_password(password)
        user.recovery_code = ''
        user.save()




