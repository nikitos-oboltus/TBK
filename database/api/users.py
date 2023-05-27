def get_users(mongo, ):
    documents = mongo.db.users.find()
    output = []
    for document in documents:
        output.append({
            '_id': str(document['_id']),
            'user_ids': document['user_ids'],
            'company_ids': document['company_ids']
        })
    return output

def get_user(mongo, id):
    document = mongo.db.users.find_one({'_id': id})
    
    if document:
        return document
    else:
        return None

def create_user(mongo, user):
    result = mongo.db.users.insert_one(user)
    return str(result.inserted_id)

def update_user(mongo, id, data):
    document = mongo.db.users.find_one({'_id': id})
    if document:
        mongo.db.users.update_one({'_id': id}, {'$set': data})
        return True
    else:
        return False

def delete_user(mongo, id):
    result = mongo.db.users.delete_one({'_id': id})
    return result.deleted_count > 0