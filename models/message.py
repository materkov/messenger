from enum import Enum


class MessageType(Enum):
    NORMAL = 1
    CONVERSATION_CREATED = 2
    USER_INVITED = 3


class Message:
    def __init__(self, id, user_id, type, body='', invited_user_id=0):
        self.id = id
        self.user_id = user_id
        self.type = type

        # normal
        self.body = body

        # user_invited
        self.invited_user_id = invited_user_id
