def get_filters(mongo):
    documents = mongo.db.filters.find()
    output = []
    for document in documents:
        output.append({
            '_id': str(document['_id']),
            'company_id': document['company_id'],
            'censored_words': document['censored_words'],
        })
    return output

def get_filters_company(mongo, company_id, active=True):
    documents = mongo.db.filters.find({'company_id': company_id, 'active': active})
    output = []
    for document in documents:
        output.append({
            '_id': str(document['_id']),
            'company_id': document['company_id'],
            'censored_words': document['censored_words'],
        })
    return output

def get_filter(mongo, id):
    document = mongo.db.filters.find_one({'_id': id})
    
    if document:
        return document
    else:
        return None

def create_filter(mongo, filter):
    result = mongo.db.filters.insert_one(filter)
    return str(result.inserted_id)

def update_filter(mongo, id, data):
    document = mongo.db.filters.find_one({'_id': id})
    if document:
        mongo.db.filters.update_one({'_id': id}, {'$set': data})
        return True
    else:
        return False

def delete_filter(mongo, id):
    result = mongo.db.filters.delete_one({'_id': id})
    return result.deleted_count > 0