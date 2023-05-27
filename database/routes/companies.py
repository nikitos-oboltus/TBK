from flask import Blueprint, current_app, jsonify, request
import uuid
from api.companies import get_companies, get_company, create_company, update_company, delete_company

# Create a blueprint object
companies_b = Blueprint('companies', __name__)

# GET request to fetch all companies
@companies_b.route('/api/companies', methods=['GET'])
def fetch_all_companies():
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    companies = get_companies(mongo)
    return jsonify({ 'companies': companies }), 200


# GET request to fetch a single company by ID
@companies_b.route('/api/companies/<id>', methods=['GET'])
def fetch_one_company(id):
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    company = get_company(mongo, id)
    if company:
        return jsonify({ 'company': company }), 200
    else:
        return jsonify({ 'message': 'Company not found' }), 404


# POST request to create a new company
@companies_b.route('/api/companies', methods=['POST'])
def add_one_company():
    company = {
        '_id': str(uuid.uuid4()),
        'token': request.json['token'],
        'tax_number': request.json['tax_number'],
        'company_name': request.json['company_name']
    }
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    company_id = create_company(mongo, company)
    return jsonify({'message': 'Company created successfully.', 'id': company_id}), 201

# PUT request to update an existing company
@companies_b.route('/api/companies/<id>', methods=['PUT'])
def update_one_company(id):
    company = {
        'token': request.json['tax_number'],
        'tax_number': request.json['tax_number'],
        'company_name': request.json['company_name']
    }
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    if (update_company(mongo, id, company)):
        return jsonify({'message': 'Company updated successfully.'}), 200
    else:
        return jsonify({'message': 'Company not found.'}), 404

# DELETE request to delete a company
@companies_b.route('/api/companies/<id>', methods=['DELETE'])
def delete_one_company(id):
    # Get mongo object from context
    with current_app.app_context():
        mongo = current_app.config['mongo']
    if (delete_company(mongo, id)):
        return jsonify({'message': 'Company deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Company not found.'}), 404
    

