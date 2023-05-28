from flask import Blueprint, current_app, jsonify, request
import uuid
from ..api.requests import get_requests, get_request, create_request, update_request, delete_request

# Create a blueprint object
requests_b = Blueprint('requests', __name__)

# GET request to fetch all responses
@requests_b.route('/api/requests', methods=['GET'])
def fetch_all_requests():
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    responses = get_requests(mongo)
    return jsonify({ 'requests': responses }), 200


# GET request to fetch a single response by ID
@requests_b.route('/api/requests/<id>', methods=['GET'])
def fetch_one_request(id):
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    response = get_request(mongo, id)
    if response:
        return jsonify({ 'requests': response }), 200
    else:
        return jsonify({ 'message': 'Request not found' }), 404


# POST request to create a new response
@requests_b.route('/api/requests', methods=['POST'])
def add_one_request():
    response = {
        '_id': str(uuid.uuid4()),
        'chat_id': request.json['chat_id'],
        'request_text': request.json['request_text'],
    }
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    request_id = create_request(mongo, response)
    return jsonify({'message': 'Request created successfully.', 'id': request_id}), 201

# PUT request to update an existing response
@requests_b.route('/api/requests/<id>', methods=['PUT'])
def update_one_response(id):
    response = {
        'chat_id': request.json['chat_id'],
        'request_text': request.json['request_text'],
    }
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    if (update_request(mongo, id, response)):
        return jsonify({'message': 'Request updated successfully.'}), 200
    else:
        return jsonify({'message': 'Request not found.'}), 404

# DELETE request to delete a response
@requests_b.route('/api/requests/<id>', methods=['DELETE'])
def delete_one_request(id):
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    if (delete_request(mongo, id)):
        return jsonify({'message': 'Request deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Request not found.'}), 404
    

