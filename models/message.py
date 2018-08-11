from enum import Enum


class MessageType(Enum):
    NORMAL = 1
    CONVERSATION_CREATED = 2


class Message:
    def __init__(self, id, user_id, body, type):
        self.id = id
        self.user_id = user_id
        self.body = body
        self.type = MessageType(type)
