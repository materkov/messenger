import asyncio
import websockets
from urllib.parse import urlparse, parse_qs
import asyncio_redis
import os

connected = {}
global_connection_counter = 1

redis_host = os.getenv('REDIS_HOST', '127.0.0.1')
redis_port = int(os.getenv('REDIS_PORT', '6379'))
app_port = int(os.getenv('PORT', '8765'))


async def get_messages():
    conn = await asyncio_redis.Connection.create(host=redis_host, port=redis_port)
    while True:
        try:
            result = await conn.blpop(['queue'], 25)
            result_parts = result.value.split(':', 2)
            if len(result_parts) != 2:
                continue

            try:
                user_ids = [int(user_id) for user_id in result_parts[0].split(',')]
            except ValueError:
                continue

            await send_all(user_ids, result_parts[1])
        except asyncio_redis.TimeoutError:
            continue


def log(msg):
    print(msg)


def on_connect(path, websocket):
    global global_connection_counter

    parsed = urlparse(path)
    qs = parse_qs(parsed.query)
    auth_token = qs['auth_token'][0] if 'auth_token' in qs else ''
    user_id = int(auth_token)

    new_conn_id = global_connection_counter
    global_connection_counter += 1

    if user_id not in connected:
        connected[user_id] = []

    connected[user_id].append(websocket)
    log(f'connected, {user_id}, conn_id: {new_conn_id}')

    return new_conn_id


def on_disconnect(conn_id):
    log(f'disconnected, {conn_id}, user {connected[conn_id][0]}')
    del connected[conn_id]


async def send_all(user_ids, message):
    sockets = []
    for user_id in user_ids:
        if user_id in connected:
            sockets += connected[user_id]

    log(f'send to , {len(sockets)}')

    if not sockets:
        return

    await asyncio.wait([websocket.send(message) for websocket in sockets])


async def serve(websocket, path):
    conn_id = on_connect(path, websocket)
    try:
        async for _ in websocket:
            await send_all('new user')
    except websockets.ConnectionClosed:
        pass
    finally:
        on_disconnect(conn_id)


asyncio.get_event_loop().run_until_complete(websockets.serve(serve, '0.0.0.0', app_port))
asyncio.ensure_future(get_messages())
asyncio.get_event_loop().run_forever()
