def get_requests(mongo, ):
    documents = mongo.db.requests.find()
    output = []
    for document in documents:
        output.append({
            '_id': str(document['_id']),
            'chat_id': document['chat_id'],
            'requests_text': document['requests_text'],
        })
    return output

def get_request(mongo, id):
    document = mongo.db.requests.find_one({'_id': id})
    
    if document:
        return document
    else:
        return None

def create_request(mongo, request):
    result = mongo.db.requests.insert_one(request)
    return str(result.inserted_id)

def update_request(mongo, id, data):
    document = mongo.db.requests.find_one({'_id': id})
    if document:
        mongo.db.requests.update_one({'_id': id}, {'$set': data})
        return True
    else:
        return False

def delete_request(mongo, id):
    result = mongo.db.requests.delete_one({'_id': id})
    return result.deleted_count > 0