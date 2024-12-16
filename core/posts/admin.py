from django.contrib import admin
from .models import Post, Interaction


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    pass