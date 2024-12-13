from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import  path
from .views import (
    SignUp, secret, ActivateAccountView,
    ResetPasswordView, SetNewPasswordView,
    LogoutView, ProfileView
)

app_name = 'account'


urlpatterns = [
    path('sign-up/', SignUp, name='sign_up'),
    path('activate/<uidb64>/<token>/', ActivateAccountView, name='activate'),
    path('sign-in/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/sign-in/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView, name='logout'),
    path('reset-password/', ResetPasswordView, name='reset_password'),
    path('set-new-password/<uidb64>/<token>/', SetNewPasswordView, name='set_new_password'),
    path('profile/', ProfileView, name='profile'),


    path('secret/', secret),

]