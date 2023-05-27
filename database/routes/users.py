from flask import Blueprint, current_app, jsonify, request
import uuid
from database.api.users import get_users, get_user, create_user, update_user, delete_user

# Create a blueprint object
users_b = Blueprint('users', __name__)

# GET request to fetch all users
@users_b.route('/api/users', methods=['GET'])
def fetch_all_users():
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    users = get_users(mongo)
    return jsonify({ 'users': users }), 200


# GET request to fetch a single user by ID
@users_b.route('/api/users/<id>', methods=['GET'])
def fetch_one_user(id):
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    user = get_user(mongo, id)
    if user:
        return jsonify({ 'user': user }), 200
    else:
        return jsonify({ 'message': 'User not found' }), 404


# POST request to create a new user
@users_b.route('/api/users', methods=['POST'])
def add_one_user():
    user = {
        '_id': str(uuid.uuid4()),
        'user_ids': request.json['user_ids'],
        'company_ids': request.json['company_ids'],
    }
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    user_id = create_user(mongo, user)
    return jsonify({'message': 'User created successfully.', 'id': user_id}), 201

# PUT request to update an existing user
@users_b.route('/api/users/<id>', methods=['PUT'])
def update_one_user(id):
    user = {
        'user_ids': request.json['user_ids'],
        'company_ids': request.json['company_ids'],
    }
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    if (update_user(mongo, id, user)):
        return jsonify({'message': 'User updated successfully.'}), 200
    else:
        return jsonify({'message': 'User not found.'}), 404

# DELETE request to delete a user
@users_b.route('/api/users/<id>', methods=['DELETE'])
def delete_one_user(id):
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    if (delete_user(mongo, id)):
        return jsonify({'message': 'User deleted successfully.'}), 200
    else:
        return jsonify({'message': 'User not found.'}), 404
    

