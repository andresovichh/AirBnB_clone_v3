#!/usr/bin/python3
""" New view for Stat objects that handles default API actions """

from flask import Flask, Blueprint, jsonify, request, url_for, abort
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from models.state import State
import json


@app_views.route("/states/<string:state_id>", methods=['GET'],
                 strict_slashes=False)
def show_with_id(state_id):
    """ shows specific class with given id """

    data = storage.get(State, state_id)
    if data is None:
        abort(404)
    return jsonify(data.to_dict())


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def show_all():
    """ by default, shows all states """

    states = storage.all(State).values()
    new_list = []
    for state in states:
        new_list.append(state.to_dict())
    return jsonify(new_list)


@app_views.route("/states/<string:state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_with_id(state_id):
    """ deletes the class associated with given id """

    data = storage.get(State, state_id)
    if data is None:
        abort(404)
    storage.delete(data)
    storage.save()
    return jsonify({}), 200
