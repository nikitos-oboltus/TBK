#!/usr/bin/env python
# coding: utf-8

# In[13]:
import threading
import pickle
import numpy as np
import pandas as pd

import flask
from flask import jsonify, request

app = flask.Flask(__name__)

FLASK_APP = 'tkb_api.py'
FLASK_ENV = 'development'

@app.route("/gettoken", methods=["GET"])
def gettoken():
    # тут должно быть процедура получающая токен и записывающая его в базу данных
    # пока возвращаем статику для тестов
    # входящие параметры id организации

    return "76f97d32-fc62-11ed-be56-0242ac120002"


@app.route("/question", methods=["GET"])
def question():
    # тут мы будем обрабатывать текст от пользователя и возвращать найденные ответы в виде массива json
    # также будем сохранять вопросы пользователя в БД
    # входящие параметры id организации id пользователя token

    result = []
    result.append({
        "id": "id ответа",
        "еtext": "какойто ответ",
    })

    return jsonify(result)


@app.route("/grade", methods=["POST"])
def grade():

    # тут получим оценку ответов и запишем её в базу также можно записать комментарий
    # входящие параметры json в катором массив свойств: id ответов, оценка, комментарий; token

    return "", 200


if __name__ == "__main__":
    app.run(host='127.0.0.1')

# In[ ]:
