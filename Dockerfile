# 使用Python 3.11官方镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    cron \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p src/static/uploads logs

# 设置权限
RUN chmod -R 755 src/static/uploads
RUN chmod +x cleanup.py

# 创建cron任务文件 - 每天凌晨2点执行清理
RUN echo "0 2 * * * cd /app && python cleanup.py >> /app/logs/cron.log 2>&1" > /etc/cron.d/cleanup-messages

# 给cron任务文件设置权限
RUN chmod 0644 /etc/cron.d/cleanup-messages

# 应用cron任务
RUN crontab /etc/cron.d/cleanup-messages

# 创建启动脚本
RUN echo '#!/bin/bash\n\
# 启动cron服务\n\
service cron start\n\
# 启动Flask应用\n\
cd /app\n\
python src/main.py' > /app/start.sh

RUN chmod +x /app/start.sh

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["/app/start.sh"]

