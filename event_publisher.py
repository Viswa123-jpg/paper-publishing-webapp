from flask_socketio import SocketIO

socketio = SocketIO()

def publish():
    socketio.emit("file_uploaded", {'message': 'hey admin you got new paper published!!!'})
    print('file_uploaded_event_published')