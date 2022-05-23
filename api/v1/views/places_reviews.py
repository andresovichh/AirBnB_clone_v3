#!/usr/bin/python3
""" this is a module to handle reviews"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route("/places/<place_id>/reviews",
                 methods=['GET'], strict_slashes=False)
def show_all_reviews():
    """shows all reviews"""

    reviews = storage.all(Place, Review)
    if reviews is None:
        abort(404)
    new_list = []
    for review in reviews.values():
        new_list.append(review.to_dict())
    return jsonify(new_list)
