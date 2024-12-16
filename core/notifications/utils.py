from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync





class NotifyUser:

    @staticmethod
    def notify_user(user, data):
        """
          Sends a real-time notification to the user via WebSocket.
        """
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_sent)(
            f'user_{user.id}',
            {
                "type": "notify.interaction",
                "data": data
            }
        )
