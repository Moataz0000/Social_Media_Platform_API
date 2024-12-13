from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.serializers import serialize
from django.shortcuts import render
from django.utils.encoding import force_bytes, force_str
from replicate.account import Account
from .serializers import SignUpSerializer, ResetPasswordSerializer, SetNewPasswordSerializer, ProfileSerializer
from .models import User, Profile
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from .tasks import send_verification_email_task, send_congratulations_email, send_reset_password_email, send_email_after_reset
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken






@api_view(['POST'])
def SignUp(request):
    data = request.data
    serialize = SignUpSerializer(data=data)
    if serialize.is_valid():
        user = serialize.save()
        user.is_active = False
        user.save()

        # Create Token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f'{settings.BASE_URL}/api/account/activate/{uid}/{token}'
        email = user.email

        # Send a verification Email with celery task
        send_verification_email_task.delay(email, activation_link)

        return Response({'message': 'Account Created Successfully. Please check you activation email'}, status=status.HTTP_201_CREATED)
    return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def ActivateAccountView(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            if user.is_active:
                email = user.email
                # Send congratulations email with celery task
                send_congratulations_email.delay(email)
                return Response({'message': 'Account activated successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'message': 'Your verification link is invalid.'}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({'message': 'secret message!'})




@api_view(['POST'])
def ResetPasswordView(request):
    data = request.data
    serialize = ResetPasswordSerializer(data=data)
    if serialize.is_valid():
        email = serialize.validated_data['email']
        try:
            user = User.objects.get(email=email)
            uid  = urlsafe_base64_encode((force_bytes(user.pk)))
            token = default_token_generator.make_token(user)
            reset_link = f'{settings.BASE_URL}/api/account/set-new-password/{uid}/{token}'
            # Send Reset Email with Celery
            send_reset_password_email.delay(email, reset_link)
            return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        except User.DoseNotExist:
            return Response({'message': 'Password not registered.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)})
    return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def SetNewPasswordView(request, uidb64, token):
    data = request.data
    serialize = SetNewPasswordSerializer(data=data)
    if serialize.is_valid():
        try:
            uid  = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                new_password = serialize.validated_data['new_password']
                user.set_password(new_password)
                user.save()
                email = user.email
                # Send a message to user with celery
                send_email_after_reset.delay(email)
                return Response({"message": 'Password reset successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def LogoutView(request):
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'message': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def ProfileView(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return Response({'error': 'Profile is not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serialize = ProfileSerializer(profile)
        return Response(serialize.data, status=status.HTTP_200_OK)

    elif request.method in ['PUT', 'PATCH']:
        data = request.data
        partial = request.method == 'PATCH'
        serialize = ProfileSerializer(profile, data=data, partial=partial)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_200_OK)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        profile.user.delete()

        return Response({'message': 'profile deleted successfully.'}, status=status.HTTP_200_OK)

    else:
        return Response({'error': 'Method is invalid.'})