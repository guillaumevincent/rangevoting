import config
from server import app


config.configure_logging()

app.repository = config.get_mongo_repository()
app.configure_handlers()

if __name__ == '__main__':
    app.run()
