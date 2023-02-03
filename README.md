# python-socketio


## ENV

- Python: 3.9^
- socketio: 4.3^

## event 정리

- connect: socket server 접속
- disconnect: socket server 접속 해제
- join: {'room_id': int, 'at': string}. 방 접속
- leave: {'room_id': int, 'at': string}. 방 나가기. 방을 나가게 되면 socket.disconnect 가 호출됨
- message: {'room_id': int, 'message': string}. 방에 메세지 전송


## 실행

- 기본
```python
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

- python-socketio
```python
python app.py
```

- flask-socketio
```python
python app2_namespace.py
```

- open browser with localhost:5000