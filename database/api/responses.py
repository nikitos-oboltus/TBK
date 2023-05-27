def get_responses(mongo, ):
    documents = mongo.db.responses.find()
    output = []
    for document in documents:
        output.append({
            '_id': str(document['_id']),
            'chat_id': document['chat_id'],
            'response_text': document['response_text'],
        })
    return output

def get_response(mongo, id):
    document = mongo.db.responses.find_one({'_id': id})
    
    if document:
        return document
    else:
        return None

def create_response(mongo, response):
    result = mongo.db.responses.insert_one(response)
    return str(result.inserted_id)

def update_response(mongo, id, data):
    document = mongo.db.responses.find_one({'_id': id})
    if document:
        mongo.db.responses.update_one({'_id': id}, {'$set': data})
        return True
    else:
        return False

def delete_response(mongo, id):
    result = mongo.db.responses.delete_one({'_id': id})
    return result.deleted_count > 0