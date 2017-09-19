import json
from channels import Group
from channels.sessions import channel_session
from urllib.parse import parse_qs
from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

# Connected to websocket.connect
@channel_session_user_from_http
def ws_add(message):
    # Accept connection
    message.reply_channel.send({"accept": True})
    print(message.user)
    # Add them to the right group
    Group("chat-%s" % message.user.username).add(message.reply_channel)

# Connected to websocket.receive
@channel_session_user
def ws_message(message):
    print(message.user.username)
    Group("chat-%s" % message.user.username).send({
        "text": message['text'],
    })

# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    Group("chat-%s" % message.user.username[0]).discard(message.reply_channel)