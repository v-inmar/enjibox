from app import create_app
from config import DevConfig, Config

app = create_app(config_class=Config)


if __name__ == "__main__":
    app.run()