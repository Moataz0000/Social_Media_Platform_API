from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Follow
from account.models import User




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, username):
    try:
        user_to_follow = User.objects.get(name=username)
        profile = user_to_follow.profile

        if profile.is_private:
            return Response({'error': 'This user has private profile.'}, status=status.HTTP_403_FORBIDDEN)

        if user_to_follow == request.user:
            return Response({"error": 'You cannot follow youself!'}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
        if created:
            return Response({'message': f'You are now following {username}'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': f'You are already following {username}'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, username):
    try:
        user_to_unfollow = User.objects.get(name=username)
        follow = Follow.objects.filter(follower=request.user, followed=user_to_unfollow)
        if follow.exists():
            follow.delete()
            return Response({'message': f'You have unfollowed {username}'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': f'You are not following {username}'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_posts(request, username):
    try:
        user = User.objects.get(name=username)
        posts = user.post_set.all()

        if user != request.user:
            posts = posts.exclude(visibility='private')
            if not Follow.objects.filter(follower=request.user, followed=user).exists():
                posts = posts.exclude(visibility='followers')
        serialize = PostSerializer(posts, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)