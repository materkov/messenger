import storage
import jwt
import bcrypt

JWT_SECRET = 'gipXZ$CB4!xcoHKa%LHZBpcy#joz'


def get_conversations_for_user(user_id):
    conversations = storage.messages.get_for_user(user_id)

    user_ids = set()
    for c in conversations:
        user_ids.add(c.last_msg.user_id)
        for user_id in c.user_ids:
            user_ids.add(user_id)

    users = storage.users.get_users(user_ids)

    return conversations, users


def create_conversation(user_ids, creator_user_id, title):
    conv_id = storage.messages.create_conversation(title, user_ids, creator_user_id)
    return conv_id


def write_conversation(conversation_id, user_id, body):
    storage.messages.add_message(conversation_id, user_id, body)


def get_messages(conversation_id: int, after: int, limit: int):
    messages = storage.messages.get_conversation_messages(conversation_id, after, limit)
    users = set()
    for m in messages:
        users.add(m.user_id)

    users = storage.users.get_users(users)
    return messages, users


def check_auth_token(auth_token):
    try:
        token = jwt.decode(auth_token, JWT_SECRET, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return 0

    try:
        return int(token.get('sub', ''))
    except ValueError:
        return 0


def generate_auth_token(user_id):
    return jwt.encode({'sub': str(user_id)}, JWT_SECRET, algorithm='HS256').decode()


def try_authorize(login, password):
    user_id, password_hash = storage.users.get_user_auth_info(login)
    if bcrypt.checkpw(password.encode(), password_hash.encode()):
        return generate_auth_token(user_id), storage.users.get_users([user_id])[user_id]
    else:
        return '', None


def register(login, name, password):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user_id = storage.users.create_user(login, name, password_hash)
    return generate_auth_token(user_id), storage.users.get_users([user_id])[user_id]


def invite_conversation(conversation_id, inviter_id, invitee_id):
    storage.messages.invite_conversation(conversation_id, inviter_id, invitee_id)
