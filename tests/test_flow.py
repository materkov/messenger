import requests
import random

HOST = 'http://localhost:5000'


def register_user(name):
    login = 'login-' + str(random.randint(1, 1000000000))
    password = '123'

    # register
    r = requests.post(HOST + "/register", json={
        'login': login,
        'name': name,
        'password': password,
    })
    assert r.status_code == 200

    auth_token = r.json()['token']
    user_id = r.json()['user']['id']
    assert len(auth_token) > 0

    return auth_token, user_id


def test_registration():
    login = 'login-' + str(random.randint(1, 1000000000))
    name = 'name-' + str(random.randint(1, 1000000000))
    password = 'password-' + str(random.randint(1, 1000000000))

    # register
    r = requests.post(HOST + "/register", json={
        'login': login,
        'name': name,
        'password': password,
    })
    assert r.status_code == 200

    auth_token = r.json()['token']
    assert len(auth_token) > 0

    user_id = r.json()['user']['id']
    assert user_id > 0
    user_name = r.json()['user']['name']
    assert user_name == name

    # bad password
    r = requests.post(HOST + "/login", json={
        'login': login,
        'password': password + 'bad',
    })
    assert r.status_code == 400
    assert r.json()['error']['error'] == 'bad_credentials'

    # correct password
    r = requests.post(HOST + "/login", json={
        'login': login,
        'password': password,
    })
    assert r.status_code == 200

    token = r.json()['token']
    assert len(token) > 0

    # create conversation
    r = requests.post(HOST + "/conversations", json={
        'user_ids': [user_id],
        'title': 'my title',
    }, headers={'Authorization': 'Bearer ' + auth_token})
    assert r.status_code == 200
    conv_id = r.json()['id']

    # write message
    r = requests.post(HOST + "/conversations/" + str(conv_id) + "/write", json={
        'body': 'olololo lolo',
    }, headers={'Authorization': 'Bearer ' + auth_token})
    assert r.status_code == 204

    # get conversations list
    r = requests.get(HOST + "/conversations", headers={'Authorization': 'Bearer ' + auth_token})
    assert r.status_code == 200

    # get conversation messages
    r = requests.get(HOST + "/conversations/" + str(conv_id) + "/messages",
                     headers={'Authorization': 'Bearer ' + auth_token})
    assert r.status_code == 200

    # invite user2
    user2_token, user2_id = register_user('user2')
    r = requests.post(HOST + "/conversations/" + str(conv_id) + "/invite",
                      headers={'Authorization': 'Bearer ' + auth_token}, json={'user_id': user2_id})
    print(r.text)
    assert r.status_code == 204

    # get conversation messages
    r = requests.get(HOST + "/conversations/" + str(conv_id) + "/messages",
                     headers={'Authorization': 'Bearer ' + auth_token})
    print(r.text)
    assert r.status_code == 200
