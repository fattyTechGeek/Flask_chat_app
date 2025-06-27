import os
import sys
# DON'T CHANGE: Add the src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
from datetime import datetime, timedelta
import secrets

# 导入数据库模型
from models.database import db, bcrypt, User, Message, Room

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SECRET_KEY'] = secrets.token_hex(16)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
db.init_app(app)
bcrypt.init_app(app)
CORS(app, origins="*")
socketio = SocketIO(app, cors_allowed_origins="*")

# 导入路由
from routes.user import user_bp
from routes.chat import chat_bp

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204

# 创建数据库表
with app.app_context():
    db.create_all()
    
    # 创建默认房间
    if not Room.query.filter_by(name='general').first():
        default_room = Room(name='general', description='默认聊天室')
        db.session.add(default_room)
        db.session.commit()

# Socket.IO事件处理
@socketio.on('connect')
def handle_connect():
    print('用户已连接')

@socketio.on('disconnect')
def handle_disconnect():
    print('用户已断开连接')
    # 更新用户在线状态
    if 'user_id' in session:
        user = User.query.session.get(User, session['user_id'])
        if user:
            user.is_online = False
            db.session.commit()

@socketio.on('join')
def handle_join(data):
    username = data.get('username')
    room = data.get('room', 'general')
    
    if 'user_id' in session:
        user = User.query.session.get(User, session['user_id'])
        if user:
            user.is_online = True
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            join_room(room)
            emit('status', {'msg': f'{username} 已加入聊天室'}, room=room)

@socketio.on('leave')
def handle_leave(data):
    username = data.get('username')
    room = data.get('room', 'general')
    
    leave_room(room)
    emit('status', {'msg': f'{username} 已离开聊天室'}, room=room)

@socketio.on('message')
def handle_message(data):
    if 'user_id' not in session:
        emit('error', {'msg': '请先登录'})
        return
    
    user = User.query.session.get(User, session['user_id'])
    if not user:
        emit('error', {'msg': '用户不存在'})
        return
    
    # 保存消息到数据库
    message = Message(
        content=data['message'],
        message_type=data.get('type', 'text'),
        room=data.get('room', 'general'),
        user_id=user.id
    )
    db.session.add(message)
    db.session.commit()
    
    # 广播消息
    message_data = {
        'id': message.id,
        'username': user.username,
        'message': data['message'],
        'timestamp': message.timestamp.strftime('%H:%M:%S'),
        'type': data.get('type', 'text'),
        'room': data.get('room', 'general')
    }
    
    emit('message', message_data, room=data.get('room', 'general'))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)

