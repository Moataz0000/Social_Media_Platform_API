from calendar import month

from rest_framework import  serializers
from .models import User, Profile


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'password')
        extra_kwargs = {
            'name': {'required': True}
        }

    def create(self, validated_data):
        name  = validated_data['name']
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects._create_user(email=email, name=name, password=password)
        return user



class MetaAiSerializer(serializers.Serializer):
    ask = serializers.CharField(max_length=1000, required=True)



class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=50, help_text='write your correct eamil to reset password.')



class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8, required=True, help_text='Write New Password.')



class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(source='get_user')

    class Meta:
        model = Profile
        fields = ('user', 'bio', 'avater', 'created', 'updated')

    def get_user(self, profile: Profile):
        if profile.user:
            return profile.user.name or profile.user.email
        return None