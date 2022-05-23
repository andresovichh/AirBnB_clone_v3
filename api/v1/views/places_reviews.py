#!/usr/bin/python3
""" this is a module to handle reviews"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review



@app_views.route("/places/<place_id>/reviews",
                 methods=['GET'], strict_slashes=False)
def show_all_reviews():
    """shows all reviews"""

    reviews = storage.all("Place", Review)
    new_list = []
    for review in reviews.values():
        new_list.append(review.to_dict())
    return jsonify(new_list)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def show_review_with_id(review_id):
    """shows review with given id"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<string:review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review_with_id(review_id):
    """deletes review with given id"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete(review)
    review.save()
    return jsonify({}), 200


@app_views.route("/places/<string:place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def show_reviews_with_place_id(place_id):
    """shows reviews with given place id"""

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = request.get_json()
    if reviews is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in reviews:
        abort(400, 'Missing user_id')
    if 'text' not in reviews:
        abort(400, 'Missing text')

    reviews.pop('id', None)
    reviews.pop('created_at', None)
    reviews.pop('updated_at', None)
    reviews.update({'place_id': place_id, "user_id": reviews['user_id']})

    reviews = Review(**reviews)
    reviews.save()
    return jsonify(reviews.to_dict()), 201


# @app_views.route("/reviews/<string:review_id>", methods=['POST'],
#                  strict_slashes=False)
# def post_review(review_id):
#     """create a new review with given id"""

#     review = storage.get(Review, review_id)
#     if review is None:
#         abort(404)
#     data = request.get_json()
#     if data is None:
#         abort(400, 'Not a JSON')
#     for key, value in data.items():
#         if key not in ['id', 'user_id', 'city_id', 'created_at',
#                        'updated_at']:
#             setattr(review, key, value)
#     review.save()
#     return jsonify(review.to_dict()), 201
