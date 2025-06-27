# Flask 实时聊天室 - 增强版

一个基于 Python Flask 框架和 Socket.IO 实现的实时聊天应用，支持用户认证、消息持久化和历史记录查看。

## 🚀 新增功能

### 用户认证系统
- **用户注册和登录**：支持用户名和密码验证
- **密码加密**：使用 bcrypt 对密码进行安全加密
- **会话管理**：支持用户登录状态保持和登出功能

### 消息持久化
- **数据库存储**：所有消息保存到 SQLite 数据库
- **历史消息**：用户登录时自动加载历史对话记录
- **消息类型**：支持文字、图片、表情等多种消息类型

### 自动清理机制
- **定时清理**：每天凌晨2点自动清理7天前的消息
- **文件清理**：同时清理相关的图片文件
- **日志管理**：清理30天前的日志文件

## 📋 功能特性

### 核心功能
- ✅ 用户注册和登录验证
- ✅ 实时消息传输（基于Socket.IO）
- ✅ 支持发送文字、图片、表情等信息
- ✅ 消息数据库持久化存储（7天）
- ✅ 历史消息自动加载
- ✅ 用户连接/断开状态提示
- ✅ 回车键快速发送

### 界面设计
- ✅ 现代化渐变色设计
- ✅ 响应式布局（支持移动端）
- ✅ 简洁美观的聊天界面
- ✅ 丰富的表情选择器
- ✅ 用户认证界面

### 技术实现
- ✅ Flask + Flask-SocketIO 后端
- ✅ SQLAlchemy 数据库ORM
- ✅ Flask-Bcrypt 密码加密
- ✅ 原生JavaScript前端
- ✅ SQLite数据库
- ✅ 图片上传功能
- ✅ 定时清理任务

### 部署支持
- ✅ Docker容器化部署
- ✅ Docker Compose编排
- ✅ 自动定时清理任务
- ✅ 详细的部署文档

## 🛠️ 技术栈

- **后端**: Python 3.11, Flask, Flask-SocketIO, SQLAlchemy, Flask-Bcrypt
- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **数据库**: SQLite
- **部署**: Docker, Docker Compose
- **定时任务**: Cron

## 📦 项目结构

```
flask-chat-app/
├── src/
│   ├── main.py                 # 主应用文件
│   ├── models/
│   │   └── database.py         # 数据库模型
│   ├── routes/
│   │   ├── user.py            # 用户认证路由
│   │   └── chat.py            # 聊天功能路由
│   └── static/
│       ├── index.html         # 前端界面
│       └── uploads/           # 图片上传目录
├── cleanup.py                 # 消息清理脚本
├── Dockerfile                 # Docker配置
├── docker-compose.yml         # Docker Compose配置
├── requirements.txt           # Python依赖
└── README.md                  # 项目说明
```

## 🚀 快速开始

### 方法一：Docker 部署（推荐）

1. **克隆项目**
   ```bash
   # 解压项目文件
   tar -xzf flask-chat-app-enhanced.tar.gz
   cd flask-chat-app
   ```

2. **启动服务**
   ```bash
   docker-compose up -d
   ```

3. **访问应用**
   - 打开浏览器访问：http://localhost:5000
   - 首次使用请先注册账号

### 方法二：本地开发

1. **安装依赖**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **启动应用**
   ```bash
   cd src
   python main.py
   ```

3. **访问应用**
   - 打开浏览器访问：http://localhost:5000

## 📱 使用说明

### 用户注册和登录
1. 首次访问时，点击"没有账号？点击注册"
2. 输入用户名和密码完成注册
3. 注册成功后自动登录进入聊天室
4. 后续访问使用已注册的账号登录

### 聊天功能
1. **发送文字消息**：在输入框输入文字，按回车或点击发送
2. **发送图片**：点击📷按钮选择图片上传
3. **发送表情**：点击😊按钮选择表情
4. **查看历史**：登录后自动加载历史消息记录

### 管理功能
- **登出**：点击右上角"登出"按钮
- **历史消息**：系统自动保存7天内的消息记录
- **自动清理**：超过7天的消息会被自动清理

## 🔧 配置说明

### 数据库配置
- 默认使用 SQLite 数据库
- 数据库文件：`chat_app.db`
- 支持自动创建表结构

### 清理任务配置
- 清理时间：每天凌晨2点
- 消息保留：7天
- 日志保留：30天

### Docker 配置
- 应用端口：5000
- 数据持久化：通过 Docker volumes
- 自动重启：容器异常时自动重启

## 🔒 安全特性

- **密码加密**：使用 bcrypt 进行密码哈希
- **会话管理**：安全的用户会话处理
- **文件上传**：限制上传文件类型和大小
- **SQL注入防护**：使用 SQLAlchemy ORM 防止 SQL 注入

## 📊 数据库结构

### 用户表 (users)
- `id`: 主键
- `username`: 用户名（唯一）
- `password_hash`: 密码哈希
- `created_at`: 创建时间

### 消息表 (messages)
- `id`: 主键
- `user_id`: 用户ID（外键）
- `content`: 消息内容
- `message_type`: 消息类型（text/image/emoji）
- `timestamp`: 发送时间

## 🐛 故障排除

### 常见问题

1. **端口占用**
   ```bash
   # 检查端口占用
   lsof -i :5000
   # 杀死占用进程
   kill -9 <PID>
   ```

2. **数据库权限**
   ```bash
   # 确保数据库目录有写权限
   chmod 755 /path/to/database/directory
   ```

3. **Docker 问题**
   ```bash
   # 重新构建镜像
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

## 📝 更新日志

### v2.0.0 (2025-06-26)
- ✨ 新增用户注册和登录功能
- ✨ 新增消息数据库持久化
- ✨ 新增历史消息查看功能
- ✨ 新增自动消息清理机制
- 🔧 优化界面布局和用户体验
- 🔧 增强安全性和数据保护

### v1.0.0
- 🎉 基础聊天功能
- 🎉 实时消息传输
- 🎉 图片和表情支持
- 🎉 Docker 部署支持

## 📄 许可证

本项目采用 MIT 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 📞 支持

如果您在使用过程中遇到问题，请：
1. 查看故障排除部分
2. 检查 Docker 容器日志
3. 提交 Issue 描述问题

