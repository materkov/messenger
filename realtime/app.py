import asyncio
import websockets
from urllib.parse import urlparse, parse_qs

connected = {}
global_connection_counter = 1


def log(msg):
    print(msg)


def on_connect(path, websocket):
    global global_connection_counter

    parsed = urlparse(path)
    qs = parse_qs(parsed.query)
    auth_token = qs['auth_token'][0] if 'auth_token' in qs else ''
    user_id = auth_token

    new_conn_id = global_connection_counter
    global_connection_counter += 1

    connected[new_conn_id] = (user_id, websocket)
    log(f'connected, {user_id}, conn_id: {new_conn_id}')

    return new_conn_id


def on_disconnect(conn_id):
    log(f'disconnected, {conn_id}, user {connected[conn_id][0]}')
    del connected[conn_id]


async def send_all():
    message = 'ololo'
    log(f'send to all, {len(connected)}')
    await asyncio.wait([websocket.send(message) for _, websocket in connected.values()])


async def serve(websocket, path):
    conn_id = on_connect(path, websocket)
    try:
        async for _ in websocket:
            await send_all()
    except websockets.ConnectionClosed:
        pass
    finally:
        on_disconnect(conn_id)


asyncio.get_event_loop().run_until_complete(websockets.serve(serve, '0.0.0.0', 8765))
asyncio.get_event_loop().run_forever()
