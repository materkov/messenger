from . import mysql
from models import User


def get_users(ids):
    if len(ids) == 0:
        return {}

    cursor = mysql.conn.cursor()

    query = "SELECT id, name FROM messenger.users WHERE id IN (" + ','.join([str(id) for id in ids]) + ")"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    users = []
    for id, name in rows:
        users.append(User(id, name))

    users_by_ids = {}
    for user in users:
        users_by_ids[user.id] = user

    return users_by_ids


def get_user_auth_info(login):
    cursor = mysql.conn.cursor()
    query = "SELECT id, password FROM messenger.users WHERE login = %s LIMIT 1"
    cursor.execute(query, (login,))
    id, password = cursor.fetchone()
    cursor.close()
    return id, password


def create_user(login, name, password_hash):
    cursor = mysql.conn.cursor()
    query = "INSERT INTO messenger.users(login, name, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (login, name, password_hash))
    id = cursor.lastrowid
    cursor.close()
    return id
