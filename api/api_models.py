import models


def convert_conversation(conversation: models.Conversation, users):
    return {
        'id': conversation.id,
        'title': conversation.title,
        'users': [convert_user(users[user_id]) for user_id in conversation.user_ids],
        'last_message': convert_message(conversation.last_msg, users[conversation.last_msg.user_id]),
    }


def convert_user(user: models.User):
    return {
        'id': user.id,
        'name': user.name,
    }


def convert_message(message: models.Message, user):
    if message.type == models.MessageType.NORMAL:
        msg_type = 'normal'
    elif message.type == models.MessageType.CONVERSATION_CREATED:
        msg_type = 'conversation_created'
    else:
        msg_type = ''

    return {
        'id': message.id,
        'type': msg_type,
        'body': message.body,
        'user': convert_user(user),
    }
