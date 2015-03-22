import sys
import logging

from flask import Flask

from bus import Bus
from repository import MockRepository
from commands import CreateRangeVotingCommand
from handlers import CreateRangeVotingHandler


def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s  %(name)12s %(levelname)7s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


class Server():
    def __init__(self, repository):
        self.app = Flask(__name__)

        configure_logging()

        self.bus = Bus()
        self.bus.register(CreateRangeVotingCommand, CreateRangeVotingHandler(repository))


if __name__ == '__main__':
    repository = MockRepository()
    server = Server(repository)
    server.app.run()