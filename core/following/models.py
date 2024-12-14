from django.utils import timezone
from django.db import models
from account.models import User



class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE, blank=True, null=True)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE, blank=True, null=True)
    created  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self) -> str:
        return f"{self.follower.name} - follows - {self.followed.name}"




class Post(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('followers', 'Followers Only'),
        ('private', 'Private')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')

    def __str__(self) -> str:
        return f'{self.user.name} - {self.content[:20]}'