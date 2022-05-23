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
def show_all_reviews(place_id):
    """shows all reviews"""

    reviews = storage.all(Place, place_id)
    if reviews is None:
        abort(404)
    new_list = []
    for review in reviews.values():
        new_list.append(review.to_dict())
    return jsonify(new_list)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def show_review_with_id(review_id):
    """shows review with given id"""

    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())
