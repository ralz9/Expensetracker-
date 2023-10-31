from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import RegisterSerializer, ChangePasswordSerializers, PasswordRecoverySerializer, PasswordRecoverySetSerializer

User = get_user_model()
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Вы успешно зарегистрировались вам отправлено пись на почту', status=201)

class ActivateAPIView(APIView):
    def get(self,request, activation_code):
        user = User.objects.get(activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Успешно ', status=200)

class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = ChangePasswordSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.set_new_password()
        return Response('Вы успешно сменили пароль', status=200)


permission_classes = [AllowAny]
class PasswordRecoveryAPIView(APIView):
    def post(self, request):
        serializer = PasswordRecoverySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response('Вам отправлненно сообщение на почту')


class PasswordRecoverySetAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordRecoverySetSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Вы успешно сменили пароль ')



