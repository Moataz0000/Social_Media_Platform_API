from asgiref.timeout import timeout
from celery.bin.control import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination





class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 5



class FeedView(APIView):
    def get(self, request):
        user = request.user
        # Caching
        cache_key = f'user_feed_{user.id}'
        feed_data = cache.get(cache_key)
        if not feed_data:
            followed_users = user.following.values_list('followed', flat=True)
            posts = Post.objects.filter(user__id__in=followed_users).order_by('-created')
            serialzier_data = PostSerializer(posts, many=True).data
            cache.set(cache_key, serialzier_data, timeout=300)
        else:
            serialzier_data = feed_data

        paginator = CustomPagination()
        paginated_feed = paginator.paginate_queryset(serialzier_data, request)

        return paginator.get_paginated_response(paginated_feed)




def clear_user_feed_cache(user):
    cache_key = f'user_feed_{user.id}'
    cache.delete(cache_key)