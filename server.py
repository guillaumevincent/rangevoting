import os
import sys
import logging

from flask import Flask, render_template, jsonify

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
        root_dir = os.path.dirname(__file__)
        self.app = Flask(__name__,
                         static_folder=os.path.join(root_dir, 'client', 'static'),
                         template_folder=os.path.join(root_dir, 'client'))
        self.app.add_url_rule('/', view_func=self.index)
        self.app.add_url_rule('/rangevotes/', view_func=self.handle_rangevotes, methods=['POST'])
        configure_logging()

        self.bus = Bus()
        self.bus.register(CreateRangeVotingCommand, CreateRangeVotingHandler(repository))

    @staticmethod
    def index():
        return render_template('index.html')

    @staticmethod
    def handle_rangevotes():

        return jsonify({'rangevotes': 0}), 201


if __name__ == '__main__':
    repository = MockRepository()
    server = Server(repository)
    server.app.run()