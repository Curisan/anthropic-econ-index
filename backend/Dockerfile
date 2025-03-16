FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建数据目录和日志目录
RUN mkdir -p /data/db /app/logs && \
    touch /data/db/app.log && \
    chmod 666 /data/db/app.log

# 设置环境变量
ENV PYTHONPATH=/app
ENV DATABASE_PATH=/data/db/database.sqlite
ENV DB_TYPE=sqlite
ENV LOG_DIR=/data/db
ENV HOST=0.0.0.0
ENV PORT=5000
# 确保在生产环境中不启用热重载
ENV DEBUG=False

# 暴露端口
EXPOSE 5000

# 创建数据卷
VOLUME ["/data/db"]

# 使用uvicorn启动，明确禁用热重载
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "5000"] 