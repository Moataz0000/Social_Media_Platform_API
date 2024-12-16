from django.urls import path
from .views import *
from .feed import FeedView


app_name = 'posts'

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('detail/<int:post_id>/<str:action>/', InteractionView.as_view(), name='post-interaction'),
    path('feed/', FeedView.as_view(), name='post-feed'),

]