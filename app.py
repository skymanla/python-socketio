from aiohttp import web
import socketio

# cors_allowed_origins -> cors 정책
# async_mode -> 비동기처리방법설정
sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)


async def index(request):
    """Serve the client-side application."""
    with open('templates/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('my_response', {'data': 'Server generated event', 'count': count})


@sio.event
async def connect(sid, environ):
    """Default session save"""
    await sio.save_session(sid, {"receive_count": 0, "room_id": 0})
    print("connect ", sid)


@sio.event
async def chat_message(sid, data):
    print("message ", data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.on("message")
def message(sid, data):
    print("Socket ID: ", sid)
    print(data)


@sio.on("join")
async def join_room(sid, data):
    sio.enter_room(sid, data['room'])

    async with sio.session(sid) as session:
        session['receive_count'] += 1
        session['room_id'] = data['room']

    await sio.emit('my_response', {'data': 'In rooms: ' + ', '.join(sio.rooms(sid)), 'count': 0})


@sio.on("leave")
async def leave_room(sid, data):
    sio.leave_room(sid, data['room'])
    async with sio.session(sid) as session:
        session['room_id'] = 0

    await sio.emit('disconnect')


@sio.event
async def my_ping(sid):
    await sio.emit('my_pong')


@sio.on("my_pong")
async def my_pong(sid):
    return True


@sio.on("my_event")
def my_event(sid, data):
    print(data)


@sio.event
async def my_room_event(sid, data):
    receive_count = 0
    async with sio.session(sid) as session:
        session['receive_count'] += 1
        receive_count = session['receive_count']

    print(await sio.get_session(sid))
    await sio.emit('my_response', {'data': data['data'], 'count': receive_count + 1}, to=data['room'])


app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
