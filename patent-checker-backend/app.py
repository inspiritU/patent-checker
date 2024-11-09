from app import create_app  # 从 __init__.py 导入 create_app 工厂函数

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    # 打印所有注册的路由（用于调试）
    print(app.url_map)
    # 启动应用
    app.run(debug=True)