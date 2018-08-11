from . import message


class Conversation:
    def __init__(self, id, title, user_ids, last_msg: message.Message):
        self.id = id
        self.title = title
        self.user_ids = user_ids
        self.last_msg = last_msg
