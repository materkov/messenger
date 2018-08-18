import flask
import json


def json_response(resp):
    return flask.Response(json.dumps(resp, indent=4))


def empty_response():
    return flask.Response(status=204)


def error_response(error, details='', status=400):
    resp = {'error': {'error': error}}
    if details:
        resp['error']['details'] = details
    resp = flask.Response(json.dumps(resp, indent=4), status=status)
    return resp


def int_or_zero(val):
    if val is None:
        return 0

    try:
        return int(val)
    except ValueError:
        return 0
