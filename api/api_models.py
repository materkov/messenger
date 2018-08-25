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
    result = {
        'id': message.id,
        'type': 'normal',
        'body': '',
        'user': convert_user(user),
        'date': message.date.isoformat() + 'Z',
    }

    if message.updated != message.created:
        result['updated'] = message.updated.isoformat() + 'Z'

    if message.type == models.MessageType.NORMAL:
        result['body'] = message.body
    elif message.type == models.MessageType.CONVERSATION_CREATED:
        result['type'] = 'conversation_created'
    elif message.type == models.MessageType.USER_INVITED:
        result['type'] = 'user_invited'
    elif message.type == models.MessageType.TITLE_CHANGED:
        result['type'] = 'title_changed'
        result['title'] = message.new_title

    return result
