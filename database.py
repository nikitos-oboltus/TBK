from flask import Flask
from flask_pymongo import PyMongo
from database.routes.companies import companies_b
from database.routes.filters import filters_b
from database.routes.ratings import ratings_b
from database.routes.responses import responses_b
from database.routes.users import users_b

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://mortymer:zyYyaCcU3RM5UuSJ@cluster0.qd1cpxu.mongodb.net/tbk?retryWrites=true&w=majority'

# Create a PyMongo instance and pass it to the app's configuration
mongo = PyMongo(app)
app.config['mongo'] = mongo

# Register the blueprints
app.register_blueprint(companies_b)
app.register_blueprint(filters_b)
app.register_blueprint(ratings_b)
app.register_blueprint(responses_b)
app.register_blueprint(users_b)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True) 