from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer, InteractionSerializer
from .post_service import PostService


class PostCreateView(APIView):
    """
    API view for creating posts.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        content = request.data.get('content')
        post_type = request.data.get('post_type')
        visibility = request.data.get('visibility')
        file = request.FILES.get('file')

        # Validate required fields
        if not content and not file:
            return Response(
                {'error': 'Content or file is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call the service to create the post
        post = PostService.create_post(user, content, post_type, visibility, file)
        return Response(
            PostSerializer(post).data,
            status=status.HTTP_201_CREATED
        )


class InteractionView(APIView):
    """
    API view for handling interactions (like, comment, share).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, action=None):
        user = request.user
        post = get_object_or_404(Post, id=post_id)

        if action == 'like':
            liked = PostService.toggle_like(user, post)  # Updated method name
            return Response(
                {'message': 'Liked' if liked else 'Unliked'},
                status=status.HTTP_200_OK
            )

        elif action == 'comment':
            content = request.data.get('content')
            if content:
                comment = PostService.comment_post(user, post, content)
                return Response(
                    InteractionSerializer(comment).data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'error': 'Comment content is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        elif action == 'share':
            shared = PostService.share_post(user, post)
            return Response(
                InteractionSerializer(shared).data,
                status=status.HTTP_201_CREATED
            )

        # Invalid action
        return Response(
            {'error': f'Invalid action: {action}. Use "like", "comment", or "share".'},
            status=status.HTTP_400_BAD_REQUEST
        )
