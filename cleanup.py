#!/usr/bin/env python3
"""
消息清理脚本
自动删除7天前的消息和相关文件
"""

import os
import sys
import sqlite3
from datetime import datetime, timedelta
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/cleanup.log'),
        logging.StreamHandler()
    ]
)

def cleanup_old_messages():
    """清理7天前的消息"""
    try:
        # 数据库路径
        db_path = '/app/chat_app.db'
        
        if not os.path.exists(db_path):
            logging.error(f"数据库文件不存在: {db_path}")
            return False
        
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 计算7天前的时间
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        seven_days_ago_str = seven_days_ago.isoformat()
        
        # 查询要删除的消息数量
        cursor.execute(
            "SELECT COUNT(*) FROM messages WHERE timestamp < ?",
            (seven_days_ago_str,)
        )
        count_to_delete = cursor.fetchone()[0]
        
        if count_to_delete == 0:
            logging.info("没有需要清理的消息")
            conn.close()
            return True
        
        # 获取要删除的图片消息
        cursor.execute(
            "SELECT content FROM messages WHERE timestamp < ? AND message_type = 'image'",
            (seven_days_ago_str,)
        )
        image_messages = cursor.fetchall()
        
        # 删除相关的图片文件
        uploads_dir = '/app/static/uploads'
        deleted_files = 0
        
        for (image_url,) in image_messages:
            if image_url.startswith('/uploads/'):
                file_path = os.path.join(uploads_dir, image_url.replace('/uploads/', ''))
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        deleted_files += 1
                        logging.info(f"删除图片文件: {file_path}")
                    except Exception as e:
                        logging.error(f"删除图片文件失败 {file_path}: {e}")
        
        # 删除过期消息
        cursor.execute(
            "DELETE FROM messages WHERE timestamp < ?",
            (seven_days_ago_str,)
        )
        
        conn.commit()
        conn.close()
        
        logging.info(f"清理完成: 删除了 {count_to_delete} 条消息和 {deleted_files} 个图片文件")
        return True
        
    except Exception as e:
        logging.error(f"清理过程中发生错误: {e}")
        return False

def cleanup_old_logs():
    """清理30天前的日志文件"""
    try:
        logs_dir = '/app/logs'
        if not os.path.exists(logs_dir):
            return True
        
        thirty_days_ago = datetime.now() - timedelta(days=30)
        deleted_logs = 0
        
        for filename in os.listdir(logs_dir):
            if filename.endswith('.log'):
                file_path = os.path.join(logs_dir, filename)
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if file_mtime < thirty_days_ago:
                    try:
                        os.remove(file_path)
                        deleted_logs += 1
                        logging.info(f"删除旧日志文件: {file_path}")
                    except Exception as e:
                        logging.error(f"删除日志文件失败 {file_path}: {e}")
        
        if deleted_logs > 0:
            logging.info(f"清理了 {deleted_logs} 个旧日志文件")
        
        return True
        
    except Exception as e:
        logging.error(f"清理日志文件时发生错误: {e}")
        return False

def main():
    """主函数"""
    logging.info("开始执行清理任务")
    
    # 确保日志目录存在
    os.makedirs('/app/logs', exist_ok=True)
    
    success = True
    
    # 清理过期消息
    if not cleanup_old_messages():
        success = False
    
    # 清理旧日志
    if not cleanup_old_logs():
        success = False
    
    if success:
        logging.info("清理任务完成")
    else:
        logging.error("清理任务执行过程中出现错误")
        sys.exit(1)

if __name__ == '__main__':
    main()

