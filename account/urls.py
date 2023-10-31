from django.contrib import admin
from django.urls import path
from .views import RegisterView, ActivateAPIView, ChangePasswordAPIView, PasswordRecoveryAPIView, PasswordRecoverySetAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<uuid:activation_code>/', ActivateAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('changepassword/', ChangePasswordAPIView.as_view()),
    path('passwordrecovery/', PasswordRecoveryAPIView.as_view()),
    path('passwordrecoveryset/', PasswordRecoverySetAPIView.as_view()),

]