from django.db import models
from account.models import User
from django.utils.translation import gettext_lazy as _



class Post(models.Model):
    class PostType(models.TextChoices):
        TEXT = 'text', _('Text')
        IMAGE = 'image', _('Image')
        VIDEO = 'video', _('Video')

    class PostVisiblility(models.TextChoices):
            PUBLIC = 'public', _('Public')
            FOLLOWERS = 'followers', _('Followers Only')
            PRIVATE = 'private', _('Private')


    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    post_type = models.CharField(max_length=10, choices=PostType.choices, default=PostType.TEXT)
    file = models.FileField(upload_to='posts/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=10, choices=PostVisiblility.choices, default=PostVisiblility.PUBLIC)

    def __str__(self) -> str:
        return f'{self.user.name} - {self.post_type}'





class Interaction(models.Model):
    class InteractionType(models.TextChoices):
        LIKE = 'like', _('Like')
        COMMENT = 'comment', _('Comment')
        SHARE = 'share', _('Share')

    user = models.ForeignKey(User, related_name='interactions', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='interactions', on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=10, choices=InteractionType.choices)
    content = models.TextField(null=True, blank=True) # For comments if is
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return str(f'{self.user.name} - {self.interaction_type} on {self.post.id}')