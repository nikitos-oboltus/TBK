def get_ratings(mongo, ):
    documents = mongo.db.ratings.find()
    output = []
    for document in documents:
        output.append({
            '_id': str(document['_id']),
            'rating': document['rating'],
            'chat_id': document['chat_id'],
            'commentary_text': document['commentary_text']
        })
    return output

def get_rating(mongo, id):
    document = mongo.db.ratings.find_one({'_id': id})
    
    if document:
        return document
    else:
        return None

def create_rating(mongo, rating):
    result = mongo.db.ratings.insert_one(rating)
    return str(result.inserted_id)

def update_rating(mongo, id, data):
    document = mongo.db.ratings.find_one({'_id': id})
    if document:
        mongo.db.ratings.update_one({'_id': id}, {'$set': data})
        return True
    else:
        return False

def delete_rating(mongo, id):
    result = mongo.db.ratings.delete_one({'_id': id})
    return result.deleted_count > 0