from rest_framework import serializers
from .models import Post, Interaction




class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(source='get_user')
    class Meta:
        model = Post
        fields = '__all__'

    def get_user(self, post: Post):
        if post.user:
            return post.user.name or post.user.email
        return None



class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = '__all__'