from .models import Post, Interaction
from notifications.utils import NotifyUser


class PostService:
    @staticmethod
    def create_post(user, content, post_type, visibility, file=None):
        """
        Creates a new post for the user.
        """
        return Post.objects.create(
            user=user,
            content=content,
            post_type=post_type,
            visibility=visibility,
            file=file
        )

    @staticmethod
    def toggle_like(user, post):
        """
        Toggles like/unlike for a post.
        Sends a notification to the post owner if liked.
        """
        interaction, created = Interaction.objects.get_or_create(
            user=user,
            post=post,
            interaction_type=Interaction.InteractionType.LIKE
        )

        if created:
            # Notify the post owner
            data = {
                "message": f"{user.name} liked your post.",
                "post_id": post.id
            }
            notify_user(post.user, data)
        else:
            interaction.delete()  # Unlike if already liked

        return created

    @staticmethod
    def comment_post(user, post, content):
        """
        Adds a comment to the post.
        Sends a notification to the post owner.
        """
        interaction = Interaction.objects.create(
            user=user,
            post=post,
            interaction_type=Interaction.InteractionType.COMMENT,
            content=content
        )

        # Notify the post owner
        data = {
            "message": f"{user.name} commented on your post.",
            "post_id": post.id
        }
        notify_user(post.user, data)

        return interaction

    @staticmethod
    def share_post(user, post):
        """
        Shares a post.
        Sends a notification to the post owner.
        """
        interaction = Interaction.objects.create(
            user=user,
            post=post,
            interaction_type=Interaction.InteractionType.SHARE
        )

        # Notify the post owner
        data = {
            "message": f"{user.name} shared your post.",
            "post_id": post.id
        }
        notify_user(post.user, data)

        return interaction
