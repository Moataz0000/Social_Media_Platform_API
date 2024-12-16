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




