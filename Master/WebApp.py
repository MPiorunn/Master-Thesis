from flask import Flask, request
import json
from random import randint
import pymongo

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

database = myclient['master']
collection = database['readings']


@app.route('/')
def hello_world():
    file = open('stasiu/data.json').read()
    jsoned = json.loads(file)
    jsoned['user'] = randint(0, 10000000)
    collection.insert(jsoned)
    return str(jsoned)


@app.route('/save', methods=["POST"])
def save():
    content = request.json
    collection.insert(content)
    return 'xD'
