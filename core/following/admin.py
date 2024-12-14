from django.contrib import admin
from .models import Follow, Post


# @admin.register(Follow)
# class FollowAdmin(admin.ModelAdmin):
#     list_display = ['follower', 'followed', 'created']
#

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ['user', 'created', 'visibility']

admin.site.register(Follow)