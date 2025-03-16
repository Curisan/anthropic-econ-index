"""
应用入口文件 - 启动FastAPI应用
"""
import uvicorn
from app import create_app
from app.core.config import HOST, PORT, DEBUG, WORKERS, RELOAD

# 创建应用实例
# 注意：在生产环境中，这个实例将被uvicorn直接使用
# 在开发环境中，如果启用了热重载，uvicorn会重新加载这个模块
app = create_app()

if __name__ == "__main__":
    # 启动应用
    print(f"启动应用: http://{HOST}:{PORT}")
    print(f"调试模式: {'开启' if DEBUG else '关闭'}")
    print(f"热重载: {'开启' if RELOAD else '关闭'}")
    
    # Uvicorn配置
    # 注意: 不支持--no-reload选项，只能设置reload=False
    uvicorn.run(
        "run:app", 
        host=HOST, 
        port=PORT, 
        reload=RELOAD,
        workers=WORKERS
    ) 