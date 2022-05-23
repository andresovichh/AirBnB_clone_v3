#!/usr/bin/python3
""" this is a module to handle reviews"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route("/places/<place_id>/reviews", methods=['GET'])
def get_place_reviews(place_id):
    """all revirews"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([rev.to_dict() for rev in place.reviews])


@app_views.route("/reviews/<review_id>", methods=['GET'])
def get_review(review_id):
    """revierwa by id"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete review by id"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200
