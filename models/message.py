from enum import Enum


class MessageType(Enum):
    NORMAL = 1
    CONVERSATION_CREATED = 2
    USER_INVITED = 3
    TITLE_CHANGED = 4


class Message:
    def __init__(self, id, user_id, type: MessageType, body='', invited_user_id=0, new_title=''):
        self.id = id
        self.user_id = user_id
        self.type = type

        # NORMAL
        self.body = body

        # USER_INVITED
        self.invited_user_id = invited_user_id

        # TITLE_CHANGED
        self.new_title = new_title
