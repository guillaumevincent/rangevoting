from flask import Flask

from bus import Bus
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