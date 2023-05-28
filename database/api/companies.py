def get_companies(mongo):
    documents = mongo.db.companies.find()
    output = []
    for document in documents:
        output.append({
            '_id': str(document['_id']),
            'token': document['tax_number'],
            'tax_number': document['tax_number'],
            'company_name': document['company_name']
        })
    return output

def get_company(mongo, id):
    document = mongo.db.companies.find_one({'_id': id})
    
    if document:
        return document
    else:
        return None

def create_company(mongo, company):
    result = mongo.db.companies.insert_one(company)
    return str(result.inserted_id)

def update_company(mongo, id, data):
    document = mongo.db.companies.find_one({'_id': id})
    if document:
        mongo.db.companies.update_one({'_id': id}, {'$set': data})
        return True
    else:
        return False

def delete_company(mongo, id):
    result = mongo.db.companies.delete_one({'_id': id})
    return result.deleted_count > 0