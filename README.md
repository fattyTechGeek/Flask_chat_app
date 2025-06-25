# Flask 实时聊天室

一个基于 Python Flask 框架和 Socket.IO 实现的现代化实时聊天应用，支持发送文字、图片、表情等多种消息类型。

## 功能特性

- ✨ **实时消息传输** - 基于 Socket.IO 的实时双向通信
- 💬 **多种消息类型** - 支持文字、图片、表情消息
- 🎨 **现代化界面** - 简洁美观的渐变色设计
- 📱 **响应式布局** - 完美适配桌面和移动设备
- ⌨️ **快捷操作** - 支持回车键快速发送消息
- 🖼️ **图片上传** - 支持多种图片格式上传和预览
- 😊 **丰富表情** - 内置表情选择器，支持快速插入表情
- 🐳 **Docker 部署** - 一键容器化部署

## 技术栈

### 后端
- **Flask** - Python Web 框架
- **Flask-SocketIO** - WebSocket 实时通信
- **SQLAlchemy** - 数据库 ORM
- **SQLite** - 轻量级数据库

### 前端
- **HTML5/CSS3** - 现代化网页技术
- **JavaScript** - 原生 JS 实现交互
- **Socket.IO Client** - 客户端实时通信

### 部署
- **Docker** - 容器化部署
- **Docker Compose** - 多容器编排

## 项目结构

```
flask-chat-app/
├── src/
│   ├── main.py              # 应用入口文件
│   ├── models/              # 数据模型
│   │   └── user.py
│   ├── routes/              # 路由处理
│   │   ├── user.py
│   │   └── chat.py          # 聊天相关 API
│   ├── static/              # 静态文件
│   │   ├── index.html       # 前端页面
│   │   └── uploads/         # 图片上传目录
│   └── database/            # 数据库文件
├── requirements.txt         # Python 依赖
├── Dockerfile              # Docker 构建文件
├── docker-compose.yml      # Docker Compose 配置
├── .dockerignore          # Docker 忽略文件
└── README.md              # 项目说明
```

## 快速开始

### 方法一：Docker 部署（推荐）

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd flask-chat-app
   ```

2. **使用 Docker Compose 启动**
   ```bash
   docker-compose up -d
   ```

3. **访问应用**
   打开浏览器访问：http://localhost:5000

### 方法二：本地开发环境

1. **环境要求**
   - Python 3.11+
   - pip

2. **安装依赖**
   ```bash
   cd flask-chat-app
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **启动应用**
   ```bash
   python src/main.py
   ```

4. **访问应用**
   打开浏览器访问：http://localhost:5000

## 使用说明

### 基本操作

1. **加入聊天室**
   - 在首页输入您的昵称
   - 点击"开始聊天"按钮进入聊天室

2. **发送消息**
   - 在输入框中输入文字消息
   - 按回车键或点击"发送"按钮发送

3. **发送表情**
   - 点击输入框右侧的表情按钮 😊
   - 从表情选择器中选择想要的表情
   - 表情会自动插入到输入框中

4. **发送图片**
   - 点击输入框右侧的相机按钮 📷
   - 选择要上传的图片文件
   - 图片会自动上传并发送到聊天室

### 支持的图片格式
- PNG
- JPG/JPEG
- GIF
- WebP

### 图片大小限制
- 最大文件大小：5MB

## 配置说明

### 环境变量

可以通过环境变量自定义应用配置：

```bash
# Flask 环境
FLASK_ENV=production

# 密钥（生产环境请更改）
SECRET_KEY=your-secret-key-here

# 数据库配置
DATABASE_URL=sqlite:///app.db
```

### Docker Compose 配置

编辑 `docker-compose.yml` 文件可以自定义：

- 端口映射
- 环境变量
- 数据卷挂载
- 网络配置

## 开发指南

### 添加新功能

1. **后端 API**
   - 在 `src/routes/` 目录下创建新的路由文件
   - 在 `src/main.py` 中注册新的蓝图

2. **Socket.IO 事件**
   - 在 `src/main.py` 中添加新的 Socket.IO 事件处理器

3. **前端功能**
   - 修改 `src/static/index.html` 添加新的 UI 组件
   - 添加相应的 JavaScript 事件处理

### 数据库操作

项目使用 SQLAlchemy ORM，数据库文件位于 `src/database/app.db`。

### 日志记录

应用日志会输出到控制台，生产环境建议配置日志文件。

## 部署到生产环境

### 使用 Docker

1. **构建镜像**
   ```bash
   docker build -t flask-chat-app .
   ```

2. **运行容器**
   ```bash
   docker run -d -p 5000:5000 --name chat-app flask-chat-app
   ```

### 使用 Docker Compose

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 反向代理配置

生产环境建议使用 Nginx 作为反向代理：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查看端口占用
   lsof -i :5000
   
   # 修改端口
   # 编辑 docker-compose.yml 或直接运行时指定端口
   ```

2. **图片上传失败**
   - 检查 `src/static/uploads/` 目录权限
   - 确认图片大小不超过 5MB
   - 检查图片格式是否支持

3. **Socket.IO 连接失败**
   - 检查防火墙设置
   - 确认 WebSocket 支持
   - 查看浏览器控制台错误信息

### 日志查看

```bash
# Docker 容器日志
docker logs flask-chat-app

# Docker Compose 日志
docker-compose logs -f flask-chat
```

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 创建 Issue
- 发送邮件
- 提交 Pull Request

---

**享受聊天的乐趣！** 🎉

