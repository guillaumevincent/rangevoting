import os
import uuid

import flask

import config
from bus import Bus, QueryDispatcher
from queries import GetRangeVoteQuery
from handlers import CreateRangeVoteHandler, GetRangeVoteHandler, UpdateRangeVoteHandler
from commands import CreateRangeVoteCommand, RangeVoteCommandValidator, UpdateRangeVoteCommand


class Server(flask.Flask):
    def __init__(self, import_name, repository=None):
        self.bus = None
        self.query_dispatcher = None

        self.repository = repository

        root_dir = os.path.dirname(__file__)
        super().__init__(import_name,
                         static_folder=os.path.join(root_dir, 'client', 'static'),
                         template_folder=os.path.join(root_dir, 'client'))

    def configure_handlers(self):
        self.bus = Bus()
        self.bus.register(CreateRangeVoteCommand, CreateRangeVoteHandler(self.repository))
        self.bus.register(UpdateRangeVoteCommand, UpdateRangeVoteHandler(self.repository))

        self.query_dispatcher = QueryDispatcher()
        self.query_dispatcher.register(GetRangeVoteQuery, GetRangeVoteHandler(self.repository))


app = Server(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/rangevotes', methods=['POST'])
def create_rangevotes():
    if RangeVoteCommandValidator(flask.request.json).is_valid():
        command = CreateRangeVoteCommand(uuid.uuid4(), flask.request.json['question'], flask.request.json['choices'])
        result = app.bus.send(command)

        if result.ok:
            rangevote_id = str(command.uuid)
            return flask.jsonify({'id': rangevote_id}), 201, {'Location': '/rangevotes/{0}'.format(rangevote_id)}

    return flask.jsonify(), 400


@app.route('/rangevotes/<path:rangevote_id>')
def get_rangevote(rangevote_id):
    query = GetRangeVoteQuery(rangevote_id)
    result = app.query_dispatcher.execute(query)
    if result:
        return flask.jsonify(result), 200
    return flask.jsonify(), 404


@app.route('/rangevotes/<path:rangevote_id>', methods=['PUT'])
def update_rangevote(rangevote_id):
    if RangeVoteCommandValidator(flask.request.json).is_valid():
        command = UpdateRangeVoteCommand(rangevote_id, flask.request.json['question'], flask.request.json['choices'])
        result = app.bus.send(command)
        if result.ok:
            return flask.jsonify(), 200
    return flask.jsonify(), 400


if __name__ == '__main__':
    config.configure_logging()
    app.repository = config.get_mongo_repository()
    app.configure_handlers()
    app.run()
