import core
from app import app
from . import api_models
from . import helpers
from flask import request
from . import auth
from flask import g


@app.route('/')
def hello():
    return 'Hello, World!'


def conversations_get():
    conversations, users = core.get_conversations_for_user(g.auth_user_id)
    conversations = [api_models.convert_conversation(c, users) for c in conversations]
    return helpers.json_response(conversations)


def conversations_post():
    body = request.get_json()
    conv_id = core.create_conversation(body['user_ids'], g.auth_user_id, body['title'])
    return helpers.json_response({'id': conv_id})


@app.route('/conversations', methods=['GET', 'POST'])
@auth.check_auth
def r_conversations():
    if request.method == 'GET':
        return conversations_get()
    elif request.method == 'POST':
        return conversations_post()


@app.route('/conversations/<conversation_id>/write', methods=['POST'])
@auth.check_auth
def r_conversations_write(conversation_id):
    body = request.get_json()
    core.write_conversation(conversation_id, g.auth_user_id, body['body'])
    return helpers.empty_response()


@app.route('/conversations/<conversation_id>/messages')
@auth.check_auth
def r_conversations_messages(conversation_id):
    after = helpers.int_or_zero(request.args.get('after'))
    limit = helpers.int_or_zero(request.args.get('limit'))
    conversation_id = helpers.int_or_zero(conversation_id)
    messages, users = core.get_messages(conversation_id, after, limit)
    result = [api_models.convert_message(m, users[m.user_id]) for m in messages]
    return helpers.json_response(result)


@app.route('/conversations/<conversation_id>/invite', methods=['POST'])
@auth.check_auth
def r_conversations_invite(conversation_id):
    body = request.get_json()
    core.invite_conversation(conversation_id, g.auth_user_id, body['user_id'])
    return helpers.empty_response()


@app.route('/conversations/<conversation_id>/entitle', methods=['POST'])
@auth.check_auth
def r_conversations_entitle(conversation_id):
    body = request.get_json()
    core.entitle_conversation(conversation_id, g.auth_user_id, body['title'])
    return helpers.empty_response()


@app.route('/login', methods=['POST'])
def r_login():
    body = request.get_json()
    login = body.get('login')
    password = body.get('password')
    auth_token, user = core.try_authorize(login, password)
    if auth_token:
        return helpers.json_response({'token': auth_token, 'user': api_models.convert_user(user)})
    else:
        return helpers.error_response('bad_credentials')


@app.route('/register', methods=['POST'])
def r_register():
    body = request.get_json()
    login = body.get('login', '')
    name = body.get('name', '')
    password = body.get('password', '')
    auth_token, user = core.register(login, name, password)
    if auth_token:
        return helpers.json_response({'token': auth_token, 'user': api_models.convert_user(user)})
    else:
        return helpers.error_response('bad_credentials')
