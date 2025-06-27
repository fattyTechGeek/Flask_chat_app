from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from models.database import db, User, Message, Room
from datetime import datetime, timedelta
import os

chat_bp = Blueprint('chat', __name__)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@chat_bp.route('/messages', methods=['GET'])
def get_messages():
    """获取历史消息"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': '未登录'}), 401
        
        room = request.args.get('room', 'general')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        # 获取7天内的消息
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        # 分页查询消息
        messages_query = Message.query.filter(
            Message.room == room,
            Message.timestamp >= seven_days_ago
        ).order_by(Message.timestamp.desc())
        
        messages_pagination = messages_query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        messages = []
        for message in reversed(messages_pagination.items):  # 反转以获得正确的时间顺序
            message_data = message.to_dict()
            messages.append(message_data)
        
        return jsonify({
            'success': True,
            'messages': messages,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': messages_pagination.total,
                'pages': messages_pagination.pages,
                'has_next': messages_pagination.has_next,
                'has_prev': messages_pagination.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'获取消息失败: {str(e)}'}), 500

@chat_bp.route('/upload', methods=['POST'])
def upload_file():
    """文件上传"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': '未登录'}), 401
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': '没有文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': '没有选择文件'}), 400
        
        if file and allowed_file(file.filename):
            # 确保上传目录存在
            upload_folder = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            
            # 生成安全的文件名
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            # 返回文件URL
            file_url = f'/uploads/{filename}'
            return jsonify({
                'success': True,
                'url': file_url,
                'filename': filename
            })
        
        return jsonify({'success': False, 'error': '不支持的文件类型'}), 400
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'文件上传失败: {str(e)}'}), 500

@chat_bp.route('/emojis', methods=['GET'])
def get_emojis():
    """获取表情列表"""
    emojis = [
        '😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇',
        '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚',
        '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩',
        '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣',
        '😖', '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡', '🤬',
        '🤯', '😳', '🥵', '🥶', '😱', '😨', '😰', '😥', '😓', '🤗',
        '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯',
        '😦', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐',
        '🥴', '🤢', '🤮', '🤧', '😷', '🤒', '🤕', '🤑', '🤠', '😈',
        '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠️', '👽', '👾'
    ]
    
    return jsonify({
        'success': True,
        'emojis': emojis
    })

@chat_bp.route('/rooms', methods=['GET'])
def get_rooms():
    """获取聊天室列表"""
    try:
        rooms = Room.query.filter_by(is_active=True).all()
        return jsonify({
            'success': True,
            'rooms': [room.to_dict() for room in rooms]
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'获取聊天室失败: {str(e)}'}), 500

@chat_bp.route('/clean-old-messages', methods=['POST'])
def clean_old_messages():
    """清理7天前的消息"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': '未登录'}), 401
        
        # 检查用户权限（可以添加管理员权限检查）
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'error': '用户不存在'}), 404
        
        # 删除7天前的消息
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        old_messages = Message.query.filter(Message.timestamp < seven_days_ago)
        deleted_count = old_messages.count()
        old_messages.delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'已清理 {deleted_count} 条过期消息'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'清理消息失败: {str(e)}'}), 500

@chat_bp.route('/message-stats', methods=['GET'])
def get_message_stats():
    """获取消息统计信息"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': '未登录'}), 401
        
        # 总消息数
        total_messages = Message.query.count()
        
        # 7天内消息数
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_messages = Message.query.filter(Message.timestamp >= seven_days_ago).count()
        
        # 今日消息数
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_messages = Message.query.filter(Message.timestamp >= today).count()
        
        # 在线用户数
        online_users = User.query.filter_by(is_online=True).count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_messages': total_messages,
                'recent_messages': recent_messages,
                'today_messages': today_messages,
                'online_users': online_users
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'获取统计信息失败: {str(e)}'}), 500

