# EasyIDPhoto 后端服务

这是一个简单的证件照处理服务，提供照片尺寸调整、背景色更改和压缩功能。

## 功能特点

- 支持1寸和2寸证件照处理
- 自定义背景颜色
- 图片压缩
- 数据库记录处理历史
- 支持SQLite和MySQL数据库
- 支持微信支付（可选）
- 健康检查和统计接口
- 基于FastAPI的现代API框架
- 自动生成API文档

## 项目结构

```
backend/
├── app/                    # 应用包
│   ├── api/                # API路由
│   │   ├── __init__.py
│   │   └── routes.py       # API端点定义
│   ├── core/               # 核心功能
│   │   ├── __init__.py
│   │   ├── config.py       # 配置管理
│   │   └── payment.py      # 支付处理
│   ├── models/             # 数据模型
│   │   ├── __init__.py
│   │   ├── database.py     # 数据库连接
│   │   └── image_record.py # 图片记录模型
│   ├── utils/              # 工具函数
│   │   ├── __init__.py
│   │   ├── image_processor.py # 图片处理
│   │   └── request_utils.py   # 请求工具
│   └── __init__.py         # 应用工厂
├── run.py                  # 应用入口
├── requirements.txt        # 依赖列表
├── Dockerfile              # Docker构建文件
└── .env                    # 环境变量配置文件
```

## API接口

### 1. 图片处理接口

- **URL**: `/process`
- **方法**: POST
- **参数**:
  - `image`: 图片文件（必须）
  - `size`: 尺寸类型，'1'=1寸，'2'=2寸（默认：'1'）
  - `background_color`: 背景颜色，如 '#FFFFFF'（默认：白色）
  - `compression`: 压缩率，0-100（默认：20）
- **返回**: 处理后的图片文件

### 2. 统计信息接口

- **URL**: `/stats`
- **方法**: GET
- **返回**: 处理统计信息，包括总数、成功数、失败数和最近记录

### 3. 健康检查接口

- **URL**: `/health`
- **方法**: GET
- **返回**: 应用健康状态信息

### 4. API文档

- **URL**: `/docs`
- **方法**: GET
- **返回**: 自动生成的API文档（Swagger UI）

## 环境变量配置

应用使用 `.env` 文件进行本地开发环境配置。在生产环境中，可以通过系统环境变量或Docker环境变量进行配置。

> **注意**: `.env` 文件不会被提交到版本控制系统中（已添加到 `.gitignore`）。如果文件不存在，应用会使用默认值或系统环境变量。新用户应该复制 `.env.example` 到 `.env` 并根据需要修改配置。

### .env 文件示例

```
# 微信支付配置
WX_APP_ID=your_wx_app_id
WX_MCH_ID=your_wx_mch_id
WX_API_KEY=your_wx_api_key
WX_NOTIFY_URL=http://your_domain/notify

# 数据库配置
DB_TYPE=sqlite
# DB_TYPE=mysql
# DB_HOST=localhost
# DB_PORT=3306
# DB_USER=root
# DB_PASSWORD=
# DB_NAME=easy_id_photo

# 应用配置
DEBUG=False
ENV=production
HOST=0.0.0.0
PORT=5000
```

### 支持的环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| ENV | 环境 | production |
| DEBUG | 调试模式 | False |
| DB_TYPE | 数据库类型 | sqlite |
| DATABASE_PATH | SQLite数据库路径 | database.sqlite |
| DB_HOST | MySQL主机 | localhost |
| DB_PORT | MySQL端口 | 3306 |
| DB_USER | MySQL用户名 | root |
| DB_PASSWORD | MySQL密码 | |
| DB_NAME | MySQL数据库名 | easy_id_photo |
| LOG_DIR | 日志目录 | /data/db |
| WX_APP_ID | 微信应用ID | |
| WX_MCH_ID | 微信商户号 | |
| WX_API_KEY | 微信API密钥 | |
| WX_NOTIFY_URL | 微信支付通知URL | |
| HOST | 服务器主机 | 0.0.0.0 |
| PORT | 服务器端口 | 5000 |

## 部署方式

### 使用Docker

```bash
# 构建镜像
docker build -t easy-id-photo-backend .

# 运行容器（SQLite）
docker run -d \
  --name easy-id-photo-backend \
  -p 5000:5000 \
  -v /data/easy-id-photo/db:/data/db \
  --restart always \
  easy-id-photo-backend

# 运行容器（MySQL）
docker run -d \
  --name easy-id-photo-backend \
  -p 5000:5000 \
  -e DB_TYPE=mysql \
  -e DB_HOST=your-mysql-host \
  -e DB_PORT=3306 \
  -e DB_USER=your-mysql-user \
  -e DB_PASSWORD=your-mysql-password \
  -e DB_NAME=your-database-name \
  --restart always \
  easy-id-photo-backend
```

### 使用GitHub Actions

项目包含GitHub Actions工作流配置，可以自动构建Docker镜像并部署到服务器。

## 开发指南

### 本地开发环境设置

1. 克隆仓库
2. 复制 `.env.example` 到 `.env` 并根据需要修改配置
3. 安装依赖：`pip install -r requirements.txt`
4. 运行应用：`python run.py`

### 添加新功能

1. 在适当的模块中添加功能
2. 更新测试
3. 提交PR

## 许可证

MIT