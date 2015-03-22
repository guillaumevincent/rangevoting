from flask import Flask

from bus import Bus
from repository import MockRepository
from commands import CreateRangeVotingCommand
from handlers import CreateRangeVotingHandler


class Server():
    def __init__(self, repository):
        self.app = Flask(__name__)
        self.app.add_url_rule('/', 'index', self.index)

        self.bus = Bus()
        self.bus.register(CreateRangeVotingCommand, CreateRangeVotingHandler(repository))

    @staticmethod
    def index():
        return "Hello World!"


if __name__ == '__main__':
    repository = MockRepository()
    server = Server(repository)
    server.app.run()