from flask import Blueprint, current_app, jsonify, request
import uuid
from database.api.responses import get_responses, get_response, create_response, update_response, delete_response

# Create a blueprint object
responses_b = Blueprint('responses', __name__)

# GET request to fetch all responses
@responses_b.route('/api/responses', methods=['GET'])
def fetch_all_responses():
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    responses = get_responses(mongo)
    return jsonify({ 'responses': responses }), 200


# GET request to fetch a single response by ID
@responses_b.route('/api/responses/<id>', methods=['GET'])
def fetch_one_response(id):
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    response = get_response(mongo, id)
    if response:
        return jsonify({ 'response': response }), 200
    else:
        return jsonify({ 'message': 'Response not found' }), 404


# POST request to create a new response
@responses_b.route('/api/responses', methods=['POST'])
def add_one_response():
    response = {
        '_id': str(uuid.uuid4()),
        'chat_id': request.json['chat_id'],
        'response_text': request.json['response_text'],
    }
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    response_id = create_response(mongo, response)
    return jsonify({'message': 'Response created successfully.', 'id': response_id}), 201

# PUT request to update an existing response
@responses_b.route('/api/responses/<id>', methods=['PUT'])
def update_one_response(id):
    response = {
        'chat_id': request.json['chat_id'],
        'response_text': request.json['response_text'],
    }
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    if (update_response(mongo, id, response)):
        return jsonify({'message': 'Response updated successfully.'}), 200
    else:
        return jsonify({'message': 'Response not found.'}), 404

# DELETE request to delete a response
@responses_b.route('/api/responses/<id>', methods=['DELETE'])
def delete_one_response(id):
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    if (delete_response(mongo, id)):
        return jsonify({'message': 'Response deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Response not found.'}), 404
    

