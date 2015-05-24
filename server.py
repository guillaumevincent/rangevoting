import os
import uuid

import flask

import bus
import queries
import handlers
import commands


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
        self.bus = bus.Bus()
        self.bus.register(commands.CreateRangeVoteCommand, handlers.CreateRangeVoteHandler(self.repository))
        self.bus.register(commands.UpdateRangeVoteCommand, handlers.UpdateRangeVoteHandler(self.repository))
        self.bus.register(commands.CreateVoteCommand, handlers.CreateVoteHandler(self.repository))

        self.query_dispatcher = bus.QueryDispatcher()
        self.query_dispatcher.register(queries.GetRangeVoteQuery, handlers.GetRangeVoteHandler(self.repository))


app = Server(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/rangevotes', methods=['POST'])
def create_rangevote():
    if commands.RangeVoteCommandValidator(flask.request.json).is_valid():
        command = commands.CreateRangeVoteCommand(uuid.uuid4(), flask.request.json['question'], flask.request.json['choices'])
        result = app.bus.send(command)
        if result.ok:
            rangevote_id = str(command.uuid)
            return flask.jsonify({'id': rangevote_id}), 201, {'Location': '/rangevotes/{0}'.format(rangevote_id)}
    return flask.jsonify(), 400


@app.route('/rangevotes/<path:rangevote_id>')
def get_rangevote(rangevote_id):
    query = queries.GetRangeVoteQuery(rangevote_id)
    rangevote = app.query_dispatcher.execute(query)
    if rangevote:
        return flask.jsonify(rangevote.serialize()), 200
    return flask.jsonify(), 404


@app.route('/rangevotes/<path:rangevote_id>', methods=['PUT'])
def update_rangevote(rangevote_id):
    if commands.RangeVoteCommandValidator(flask.request.json).is_valid():
        command = commands.UpdateRangeVoteCommand(rangevote_id, flask.request.json['question'], flask.request.json['choices'])
        result = app.bus.send(command)
        if result.ok:
            return flask.jsonify(), 200
    return flask.jsonify(), 400


@app.route('/rangevotes/<path:rangevote_id>/votes', methods=['POST'])
def create_vote(rangevote_id):
    if commands.VoteCommandValidator(flask.request.json).is_valid():
        command = commands.CreateVoteCommand(rangevote_id, flask.request.json['elector'], flask.request.json['opinions'])
        result = app.bus.send(command)
        if result.ok:
            return flask.jsonify({'id': rangevote_id}), 201, {'Location': '/rangevotes/{0}'.format(rangevote_id)}
    return flask.jsonify(), 400
