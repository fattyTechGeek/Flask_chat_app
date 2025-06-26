import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
from src.models.user import db
from src.routes.user import user_bp
from src.routes.chat import chat_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# 初始化SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


# Socket.IO事件处理
@socketio.on('connect')
def handle_connect():
    print('用户已连接')
    emit('status', {'msg': '已连接到聊天服务器'})

@socketio.on('disconnect')
def handle_disconnect():
    print('用户已断开连接')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data.get('room', 'general')
    join_room(room)
    emit('status', {'msg': f'{username} 已加入聊天室'}, room=room)

@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data.get('room', 'general')
    leave_room(room)
    emit('status', {'msg': f'{username} 已离开聊天室'}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data.get('room', 'general')
    emit('message', {
        'username': data['username'],
        'message': data['message'],
        'timestamp': data['timestamp'],
        'type': data.get('type', 'text')
    }, room=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', allow_unsafe_werkzeug=True, port=5000, debug=True)
