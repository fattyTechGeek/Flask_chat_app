from flask import Blueprint, request, jsonify, session
from models.database import db, User
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        # 验证输入
        if not username or not password:
            return jsonify({'success': False, 'error': '用户名和密码不能为空'}), 400
        
        if len(username) < 3 or len(username) > 20:
            return jsonify({'success': False, 'error': '用户名长度必须在3-20个字符之间'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'error': '密码长度至少6个字符'}), 400
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'error': '用户名已存在'}), 400
        
        # 创建新用户
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '注册成功',
            'user': user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'注册失败: {str(e)}'}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        # 验证输入
        if not username or not password:
            return jsonify({'success': False, 'error': '用户名和密码不能为空'}), 400
        
        # 查找用户
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify({'success': False, 'error': '用户名或密码错误'}), 401
        
        # 设置会话
        session['user_id'] = user.id
        session['username'] = user.username
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        user.is_online = True
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '登录成功',
            'user': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'登录失败: {str(e)}'}), 500

@user_bp.route('/logout', methods=['POST'])
def logout():
    """用户登出"""
    try:
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            if user:
                user.is_online = False
                db.session.commit()
            
            session.clear()
        
        return jsonify({'success': True, 'message': '登出成功'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'登出失败: {str(e)}'}), 500

@user_bp.route('/profile', methods=['GET'])
def get_profile():
    """获取用户信息"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': '未登录'}), 401
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'error': '用户不存在'}), 404
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'获取用户信息失败: {str(e)}'}), 500

@user_bp.route('/check-auth', methods=['GET'])
def check_auth():
    """检查用户认证状态"""
    try:
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            if user:
                return jsonify({
                    'success': True,
                    'authenticated': True,
                    'user': user.to_dict()
                })
        
        return jsonify({
            'success': True,
            'authenticated': False
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'检查认证状态失败: {str(e)}'}), 500

@user_bp.route('/online-users', methods=['GET'])
def get_online_users():
    """获取在线用户列表"""
    try:
        online_users = User.query.filter_by(is_online=True).all()
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in online_users]
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'获取在线用户失败: {str(e)}'}), 500

