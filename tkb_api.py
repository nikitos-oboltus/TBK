import time
from datetime import timedelta
import flask
from flask import jsonify, request
from flask_pymongo import PyMongo

import uuid

from database.api.companies import get_companies, get_company, create_company, update_company, delete_company
from database.api.filters import get_filters, get_filter, create_filter, update_filter, delete_filter
from database.api.ratings import get_ratings, get_rating, create_rating, update_rating, delete_rating
from database.api.responses import get_responses, get_response, create_response, update_response, delete_response
from database.api.users import get_users, get_user, create_user, update_user, delete_user

from database.routes.companies import companies_b
from database.routes.filters import filters_b
from database.routes.ratings import ratings_b
from database.routes.responses import responses_b
from database.routes.users import users_b

app = flask.Flask(__name__)

FLASK_APP = 'tkb_api.py'
FLASK_ENV = 'development'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=10)

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

TEST_TOKEN = "76f97d32-fc62-11ed-be56-0242ac120002"
ID = "333"

def verification(req):

    token = req.headers.get("token", type=str)
    id = req.args.get("id", type=str)

    # тут должна быть проверка совпадения id и token по БД

    company = get_company(mongo, id)

    if token != company["token"] and id == company["_id"]:
        return "API ключ недействительный (у компании нет доступа к сервису)", False

    else:
        # тут обработка по фильтру
        return "", True

@app.route("/gettoken", methods=["GET"])
def gettoken():

    time_stamp = time.time()
    inn = request.args.get("inn", type=str)
    name = request.args.get("name", type=str)

    if inn != "" and name != "":

        # тут должна быть процедура получающая токен и id компании также записывающая их в БД
        # пока возвращаем статику для тестов
        # входящие параметры inn(ИНН) и name(Название) организации

        token = uuid.uuid4()

        company = {
            '_id': str(uuid.uuid4()),
            'token': str(token),
            'tax_number': inn,
            'company_name': name
        }

        id = create_company(mongo, company)

        result = []
        result.append({
            "id": id,
            "token": token,
        })

        return jsonify(result)

    else:
        return "Не создан token (ИНН и Имя компании не должны быть пустыми)", True



@app.route("/question", methods=["GET"])
def question():
    time_stamp = time.time()

    error, ver = verification(request)

    if ver:

        id = request.args.get("id", type=str)
        iduser = request.args.get("iduser", type=str)
        q = request.args.get("q", type=str) # надо проверить текст через фильтры

        # тут мы будем обрабатывать текст от пользователя и возвращать найденные ответы в виде массива json
        # также будем сохранять вопросы пользователя в БД
        # входящие параметры: , id - компании, iduser - ид пользователя, token - ключ

        if iduser != "":

            response = {
                '_id': str(uuid.uuid4()),
                'chat_id': iduser,
                'response_text': q,
            }

            response_id = create_response(mongo, response)

            # тут должен быть механизм поиска ответов

            result = []
            result.append({
                "id": "id ответа",
                "еtext": "какойто ответ",
            })

            return jsonify(result)

    else:
        return jsonify(error)


@app.route("/grade", methods=["POST"])
def grade():
    time_stamp = time.time()
    error, ver = verification(request)

    if ver:

        iduser = request.args.get("iduser", type=str)

        data = request.get_json()

        for grd in data["grades"]:
            id_answer = grd["id"]
            grd_answer = grd["grade"]
            com_answer = grd["comment"]

            rating = {
                '_id': str(uuid.uuid4()),
                'rating': grd_answer,
                'chat_id': iduser,
                'rating_id': id_answer,
                'commentary_text': com_answer
            }

            rating_id = create_rating(mongo, rating)

        # тут получим оценку и комментарий(не обязательно) ответов и запишем её в БД
        # входящие параметры json в катором массив свойств: id ответов, оценка, комментарий; token - ключ, id - компании
        # можно реализовать уточняющие вопросы

        return "", 200

    else:
        return jsonify(error)

@app.route("/filter", methods=["POST"])
def setfilter():
    time_stamp = time.time()
    error, ver = verification(request)

    if ver:
        data = request.get_json()

        # тут устанавливаем список слов для фильтрации
        # входящие параметры: json в катором массив слов; token - ключ, id - компании
        # возвращаем idfilter

        idfilter = ""

        return idfilter

    else:
        return jsonify(error)

@app.route("/filter", methods=["GET"])
def getfilter():

    error, ver = verification(request)

    if ver:
        # тут получает список слов фильтра
        # входящие параметры: idfilter; token - ключ, id - компании
        # возвращаем json в катором массив слов

        result = []
        result.append({
            "idfilter": "id фильтра",
            "list": "список слов",
        })

        return jsonify(error)

    else:
        return jsonify(error)

@app.route("/filter", methods=["DELETE"])
def delfilter():
    time_stamp = time.time()
    error, ver = verification(request)

    if ver:

        idfilter = request.args.get("idfilter", type = str)
        if idfilter != "":
            # тут архивируем фильтр
            # входящие параметры: idfilter; token - ключ, id - компании
            return "", 200

        return "Фильтр не найден (ИД фильтра не должн быть пустым)", 200

    else:
        return jsonify(error)

@app.errorhandler(408)
def timeout(e):
    return jsonify("Запрос не удалось обработать в срок, timeout")

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')
