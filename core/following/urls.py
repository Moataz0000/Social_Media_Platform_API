from django.urls import path
from .views import (
    follow_user, unfollow_user
)

app_name = 'following'



urlpatterns = [
    path('follow/<str:username>/', follow_user, name='follow_user'),
    path('unfollow/<str:username>/', unfollow_user, name='unfollow_user'),
]