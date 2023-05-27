from flask import Blueprint, current_app, jsonify, request
import uuid
from api.filters import get_filters, get_filter, create_filter, update_filter, delete_filter

# Create a blueprint object
filters_b = Blueprint('filters', __name__)

# GET request to fetch all filters
@filters_b.route('/api/filters', methods=['GET'])
def fetch_all_filters():
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    filters = get_filters(mongo)
    return jsonify({ 'filters': filters }), 200


# GET request to fetch a single filter by ID
@filters_b.route('/api/filters/<id>', methods=['GET'])
def fetch_one_filter(id):
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    filter = get_filter(mongo, id)
    if filter:
        return jsonify({ 'filter': filter }), 200
    else:
        return jsonify({ 'message': 'Filter not found' }), 404


# POST request to create a new filter
@filters_b.route('/api/filters', methods=['POST'])
def add_one_filter():
    filter = {
        '_id': str(uuid.uuid4()),
        'company_id': request.json['company_id'],
        'censored_words': request.json['censored_words'],
    }
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    filter_id = create_filter(mongo, filter)
    return jsonify({'message': 'Filter created successfully.', 'id': filter_id}), 201

# PUT request to update an existing filter
@filters_b.route('/api/filters/<id>', methods=['PUT'])
def update_one_filter(id):
    filter = {
        'company_id': request.json['company_id'],
        'censored_words': request.json['censored_words'],
    }
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    if (update_filter(mongo, id, filter)):
        return jsonify({'message': 'Filter updated successfully.'}), 200
    else:
        return jsonify({'message': 'Filter not found.'}), 404

# DELETE request to delete a filter
@filters_b.route('/api/filters/<id>', methods=['DELETE'])
def delete_one_filter(id):
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    if (delete_filter(mongo, id)):
        return jsonify({'message': 'Filter deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Filter not found.'}), 404
    

