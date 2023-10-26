from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import RegisterSerializer

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


class ChangePassword(APIView):
    def post(self, request):
        serializers = ...
        pass