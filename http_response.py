import json
import flask


def jsonify(response=None, status=None, headers=None, mimetype='application/json; charset=utf-8'):
    json_response = json.dumps(response)
    return flask.Response(response=json_response, status=status, headers=headers, mimetype=mimetype)


def not_found():
    return flask.Response(status=404)


def bad_request():
    return flask.Response(status=400)
