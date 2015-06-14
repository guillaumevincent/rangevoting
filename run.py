import config
import server


config.configure_logging()

server.app.repository = config.get_mongo_repository()
server.app.configure_handlers()

app = server.app

if __name__ == '__main__':
    server.app.run()
