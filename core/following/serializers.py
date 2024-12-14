from rest_framework import serializers
from .models import Post



class PostSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'content', 'created', 'visibility']