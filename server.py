import os
import sys
import logging
import uuid

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from smartconfigparser import Config

from bus import Bus, QueryDispatcher
from queries import GetRangeVoteQuery
from repository import MongoRepository
from handlers import CreateRangeVoteHandler, GetRangeVoteHandler
from commands import CreateRangeVoteCommand, CreateRangeVoteCommandValidator


logger = logging.getLogger(__name__)


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
        self.app.add_url_rule('/rangevotes', view_func=self.create_rangevotes, methods=['POST'])
        self.app.add_url_rule('/rangevotes/<path:rangevote_id>', view_func=self.get_rangevote, methods=['GET'])

        configure_logging()

        self.bus = Bus()
        self.bus.register(CreateRangeVoteCommand, CreateRangeVoteHandler(repository))

        self.query_dispatcher = QueryDispatcher()
        self.query_dispatcher.register(GetRangeVoteQuery, GetRangeVoteHandler(repository))

    @staticmethod
    def index():
        return render_template('index.html')

    def create_rangevotes(self):
        if CreateRangeVoteCommandValidator(request.json).is_valid():
            command = CreateRangeVoteCommand(uuid.uuid4(), request.json['question'], request.json['choices'])
            result = self.bus.send(command)

            if result.ok:
                rangevote_id = str(command.uuid)
                return jsonify({'id': rangevote_id}), 201, {'Location': '/rangevotes/{0}'.format(rangevote_id)}

        return jsonify(), 400

    def get_rangevote(self, rangevote_id):
        query = GetRangeVoteQuery(rangevote_id)
        result = self.query_dispatcher.execute(query)
        if result:
            return jsonify(result), 200
        return jsonify(), 404


def get_mongo_repository():
    config = Config()
    config.read('config.ini')
    host = config.get('DATABASE', 'host', 'localhost')
    port = config.getint('DATABASE', 'port', 27017)
    try:
        db = MongoClient(host, port)['rangevoting']
        return MongoRepository(db)
    except Exception as e:
        logger.exception('mongo db is not started on mongodb://{0}:{1}/'.format(host, port))
        sys.exit()


if __name__ == '__main__':
    repository = get_mongo_repository()
    server = Server(repository)
    server.app.run()