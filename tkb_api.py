import time
import flask
from flask import jsonify, request

app = flask.Flask(__name__)

FLASK_APP = 'tkb_api.py'
FLASK_ENV = 'development'
TEST_TOKEN = "76f97d32-fc62-11ed-be56-0242ac120002"
ID = "333"

def verification(req):

    token = req.headers.get("token", type=str)
    id = req.args.get("id", type=str)

    # тут должна быть проверка совпадения id и token по БД

    if token != TEST_TOKEN and id == ID:
        return "API ключ недействительный (у компании нет доступа к сервису)", False

    else:
        # тут обработка по фильтру
        return "", True

@app.route("/gettoken", methods=["GET"])
def gettoken():
    time_stamp = time.time()
    id = request.args.get("inn", type=str)
    name = request.args.get("name", type=str)

    if id != "" and name != "":
        # тут должна быть процедура получающая токен и id компании также записывающая их в БД
        # пока возвращаем статику для тестов
        # входящие параметры inn(ИНН) и name(Название) организации

        result = []
        result.append({
            "id": ID,
            "token": TEST_TOKEN,
        })

        return jsonify(result)

    else:
        return "Не создан token (ИНН и Имя компании не должны быть пустыми)", True



@app.route("/question", methods=["GET"])
def question():

    error, ver = verification(request)

    if ver:
        # тут мы будем обрабатывать текст от пользователя и возвращать найденные ответы в виде массива json
        # также будем сохранять вопросы пользователя в БД
        # входящие параметры: , id - компании, iduser - ид пользователя, token - ключ

        iduser = request.args.get("iduser", type=str)

        if iduser != "":

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

    error, ver = verification(request)

    if ver:

        data = request.get_json()

        for grd in data["grades"]:
            id_answer = grd["id"]
            grd_answer = grd["grade"]
            com_answer = grd["comment"]
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

if __name__ == "__main__":
    app.run(host='127.0.0.1')

