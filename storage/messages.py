import time
import collections
from . import mysql
import sys
import models


def get_for_user(user_id):
    cursor = mysql.conn.cursor()

    # Select conversation_ids and last_msg_ids
    query = "SELECT conversation_id, last_msg_id FROM messenger.conversations_users WHERE user_id = %s ORDER BY last_msg_id DESC"
    cursor.execute(query, (user_id,))
    rows1 = cursor.fetchall()
    conversation_ids = [conv_id for conv_id, _ in rows1]
    conversation_ids_str = ','.join([str(conv_id) for conv_id, _ in rows1])
    consersation_last_msg_ids = {conv_id: msg_id for conv_id, msg_id in rows1}
    msg_ids_str = ','.join(str(msg_id) for _, msg_id in rows1)

    # Select conversations data
    query = "SELECT id, title FROM messenger.conversations WHERE id IN (" + conversation_ids_str + ")"
    cursor.execute(query)
    rows2 = cursor.fetchall()

    # Select users in this conversations
    query = "SELECT conversation_id, user_id FROM messenger.conversations_users WHERE conversation_id IN (" + conversation_ids_str + ")"
    cursor.execute(query)
    rows3 = cursor.fetchall()

    conversations_users = collections.defaultdict(set)
    for conversation_id, user_id in rows3:
        conversations_users[conversation_id].add(user_id)

    # Select messages data
    query = "SELECT id, user_id, body, type FROM messenger.messages WHERE id IN (" + msg_ids_str + ")"
    cursor.execute(query)
    rows4 = cursor.fetchall()

    messages = {id: models.Message(id, user_id, body, type) for id, user_id, body, type in rows4}

    conversations = {}
    for id, title in rows2:
        user_ids = conversations_users.get(id) or []
        last_msg = messages[consersation_last_msg_ids[id]]
        conversations[id] = models.Conversation(id, title, user_ids, last_msg)

    return [conversations[conv_id] for conv_id in conversation_ids]


def create_conversation(title, user_ids, creator_user_id):
    cursor = mysql.conn.cursor()

    query = "INSERT INTO messenger.conversations(title) VALUES (%s)"
    cursor.execute(query, (title,))
    conv_id = cursor.lastrowid

    query = "INSERT INTO messenger.messages(conversation_id, user_id, body, type) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (conv_id, creator_user_id, '', models.MessageType.CONVERSATION_CREATED.value))
    msg_id = cursor.lastrowid

    for user_id in user_ids:
        query = "INSERT INTO messenger.conversations_users(conversation_id, user_id, last_msg_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (conv_id, user_id, msg_id))

    cursor.close()

    return conv_id


def add_message(conversation_id, user_id, body, msg_type=models.MessageType.NORMAL):
    cursor = mysql.conn.cursor()

    query = "INSERT INTO messenger.messages(conversation_id, user_id, body, type) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (conversation_id, user_id, body, msg_type.value))
    msg_id = cursor.lastrowid

    query = "UPDATE messenger.conversations_users SET last_msg_id = %s WHERE conversation_id = %s"
    cursor.execute(query, (msg_id, conversation_id))

    cursor.close()

    return msg_id


def get_conversation_messages(conversation_id: int, after: int, limit: int):
    if after:
        after_clause = 'AND id < %d' % after
    else:
        after_clause = ''

    limit = 20

    cursor = mysql.conn.cursor()
    query = "SELECT id, user_id, body, type FROM messenger.messages WHERE conversation_id = %d %s ORDER BY id DESC LIMIT %d" % \
            (conversation_id, after_clause, limit)
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    result = []
    for id, user_id, body, type in rows:
        result.append(models.Message(id, user_id, body, type))

    return result


def unserialize_message(id, user_id, type, body):
    if type == models.MessageType.NORMAL.value:
        return models.Message(id, user_id, models.MessageType.NORMAL, body=body)
    elif type == models.MessageType.CONVERSATION_CREATED.value:
        return models.Message(id, user_id, models.MessageType.CONVERSATION_CREATED)
    elif type == models.MessageType.USER_INVITED.value:
        return models.Message(id, user_id, models.MessageType.USER_INVITED, invited_user_id=0)
    else:
        return models.Message(id, user_id, models.MessageType.NORMAL)


def serialize_message(msg):
    body = ''
    if msg is models.NormalMessage:
        body = msg.body
    elif msg is models.UserInvitedMessage:
        body = str(msg.invited_user_id)

    return msg.user_id, msg.type.value, body


def invite_conversation(conversation_id, inviter_id, invitee_id):
    msg_id = add_message(conversation_id, inviter_id, '', models.MessageType.USER_INVITED)

    cursor = mysql.conn.cursor()
    query = "INSERT INTO messenger.conversations_users(conversation_id, user_id, last_msg_id) VALUES (%s, %s, %s)"
    cursor.execute(query, (conversation_id, invitee_id, msg_id))
