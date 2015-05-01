import os
import uuid

import flask

import config
from bus import Bus, QueryDispatcher
from queries import GetRangeVoteQuery
from handlers import CreateRangeVoteHandler, GetRangeVoteHandler, UpdateRangeVoteHandler
from commands import CreateRangeVoteCommand, RangeVoteCommandValidator, UpdateRangeVoteCommand


class Server():
    def __init__(self, repository):
        root_dir = os.path.dirname(__file__)
        self.app = flask.Flask(__name__,
                               static_folder=os.path.join(root_dir, 'client', 'static'),
                               template_folder=os.path.join(root_dir, 'client'))
        self.app.add_url_rule('/', view_func=self.index)
        self.app.add_url_rule('/rangevotes', view_func=self.create_rangevotes, methods=['POST'])
        self.app.add_url_rule('/rangevotes/<path:rangevote_id>', view_func=self.get_rangevote, methods=['GET'])
        self.app.add_url_rule('/rangevotes/<path:rangevote_id>', view_func=self.update_rangevote, methods=['PUT'])

        self.bus = Bus()
        self.bus.register(CreateRangeVoteCommand, CreateRangeVoteHandler(repository))
        self.bus.register(UpdateRangeVoteCommand, UpdateRangeVoteHandler(repository))

        self.query_dispatcher = QueryDispatcher()
        self.query_dispatcher.register(GetRangeVoteQuery, GetRangeVoteHandler(repository))

    def run(self):
        self.app.run()

    @staticmethod
    def index():
        return flask.render_template('index.html')

    def create_rangevotes(self):
        if RangeVoteCommandValidator(flask.request.json).is_valid():
            command = CreateRangeVoteCommand(uuid.uuid4(), flask.request.json['question'], flask.request.json['choices'])
            result = self.bus.send(command)

            if result.ok:
                rangevote_id = str(command.uuid)
                return flask.jsonify({'id': rangevote_id}), 201, {'Location': '/rangevotes/{0}'.format(rangevote_id)}

        return flask.jsonify(), 400

    def update_rangevote(self, rangevote_id):
        if RangeVoteCommandValidator(flask.request.json).is_valid():
            command = UpdateRangeVoteCommand(rangevote_id, flask.request.json['question'], flask.request.json['choices'])
            result = self.bus.send(command)
            if result.ok:
                return flask.jsonify(), 200
        return flask.jsonify(), 400

    def get_rangevote(self, rangevote_id):
        query = GetRangeVoteQuery(rangevote_id)
        result = self.query_dispatcher.execute(query)
        if result:
            return flask.jsonify(result), 200
        return flask.jsonify(), 404


if __name__ == '__main__':
    config.configure_logging()
    mongo_repository = config.get_mongo_repository()
    Server(mongo_repository).run()