from app import server
from app.handlers import user_bp


server.register_blueprint(user_bp)


if __name__ == '__main__':
    server.run()
