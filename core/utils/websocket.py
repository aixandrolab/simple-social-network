from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_group_message(group_name, message_type):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': message_type,
        }
    )
