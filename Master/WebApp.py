import json
import os
from random import randint

from flask import Flask, request
from pymongo import MongoClient

'''
run localhost:5000
'''
app = Flask(__name__)

myclient = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)

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


if __name__ == "__main__":
    app.run(host='0.0.0.0')
