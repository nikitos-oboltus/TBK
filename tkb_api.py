import flask
from flask import jsonify, request

app = flask.Flask(__name__)

FLASK_APP = 'tkb_api.py'
FLASK_ENV = 'development'
TEST_TOKEN = "76f97d32-fc62-11ed-be56-0242ac120002"
ID = "333"

def verification(req):

    token = req.get("token")
    id = req.get("id")

    # тут должна быть проверка совпадения id и token по БД

    if token != TEST_TOKEN and id == ID:
        return "API ключ недействительный (у компании нет доступа к сервису)", False

    else:
        # тут обработка по фильтру
        return "", True

@app.route("/gettoken", methods=["GET"])
def gettoken():

    id = request.args.get("inn")
    name = request.args.get("name")

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
        return "Не создан token (ИНН и Имя компании не должны быть пустыми) ", True



@app.route("/question", methods=["GET"])
def question():

    error, ver = verification(request)

    if ver:
        # тут мы будем обрабатывать текст от пользователя и возвращать найденные ответы в виде массива json
        # также будем сохранять вопросы пользователя в БД
        # входящие параметры: id - ид организации, iduser - ид пользователя, token - ключ

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
        # тут получим оценку и комментарий(не обязательно) ответов и запишем её в БД
        # входящие параметры json в катором массив свойств: id ответов, оценка, комментарий; token - ключ

        return "", 200

    else:
        return jsonify(error)

@app.route("/filter", methods=["POST"])
def setfilter():
    # тут устанавливаем список слов для фильтрации
    # входящие параметры: json в катором массив слов; token - ключ
    # возвращаем idfilter
    pass

@app.route("/filter", methods=["GET"])
def getfilter():
    # тут получает список слов фильтра
    # входящие параметры: idfilter; token - ключ
    # возвращаем json в катором массив слов
    pass

@app.route("/filter", methods=["DELETE"])
def delfilter():
    # тут архивируем фильтр
    # входящие параметры: idfilter; token - ключ
    pass

if __name__ == "__main__":
    app.run(host='127.0.0.1')

