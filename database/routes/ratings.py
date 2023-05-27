from flask import Blueprint, current_app, jsonify, request
import uuid
from database.api.ratings import get_ratings, get_rating, create_rating, update_rating, delete_rating

# Create a blueprint object
ratings_b = Blueprint('ratings', __name__)

# GET request to fetch all ratings
@ratings_b.route('/api/ratings', methods=['GET'])
def fetch_all_ratings():
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    ratings = get_ratings(mongo)
    return jsonify({ 'ratings': ratings }), 200


# GET request to fetch a single rating by ID
@ratings_b.route('/api/ratings/<id>', methods=['GET'])
def fetch_one_rating(id):
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    rating = get_rating(mongo, id)
    if rating:
        return jsonify({ 'rating': rating }), 200
    else:
        return jsonify({ 'message': 'Rating not found' }), 404


# POST request to create a new rating
@ratings_b.route('/api/ratings', methods=['POST'])
def add_one_rating():
    rating = {
        '_id': str(uuid.uuid4()),
        'rating': request.json['rating'],
        'chat_id': request.json['chat_id'],
        'commentary_text': request.json['commentary_text']
    }
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    rating_id = create_rating(mongo, rating)
    return jsonify({'message': 'Rating created successfully.', 'id': rating_id}), 201

# PUT request to update an existing rating
@ratings_b.route('/api/ratings/<id>', methods=['PUT'])
def update_one_rating(id):
    rating = {
        'rating': request.json['rating'],
        'chat_id': request.json['chat_id'],
        'commentary_text': request.json['commentary_text']
    }
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    if (update_rating(mongo, id, rating)):
        return jsonify({'message': 'Rating updated successfully.'}), 200
    else:
        return jsonify({'message': 'Rating not found.'}), 404

# DELETE request to delete a rating
@ratings_b.route('/api/ratings/<id>', methods=['DELETE'])
def delete_one_rating(id):
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    if (delete_rating(mongo, id)):
        return jsonify({'message': 'Rating deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Rating not found.'}), 404
    

