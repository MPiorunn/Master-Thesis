import json
import numpy as np
import datetime
import pandas as pd
from flask import Flask, request
from pymongo import MongoClient

'''
run localhost:5000
'''
app = Flask(__name__)

myclient = MongoClient("mongodb://localhost:27017/")
# DOCKER-COMPOSE
# = MongoClient(
# os.environ['DB_PORT_27017_TCP_ADDR'],
# 27017)

database = myclient['master']
collection = database['readings']


@app.route('/save', methods=["POST"])
def save():
    content = request.json
    collection.insert_one(content)
    return content


@app.route('/get', methods=["GET"])
def get():
    name = request.args.get("name")
    readings = []
    document = collection.find({"name": name})
    for doc in document:
        readings.append(str(doc))
    stringed = json.dumps(readings)
    return stringed


if __name__ == "__main__":
    app.run(host='0.0.0.0')


# never use this method!

def read_files_save_all():
    ja = "ja"
    mrozek = "mrozek"
    stasiu = "stasiu"
    maciek = "maciek"
    for i in range(1, 6):
        name = ja + "/data" + str(i) + ".txt"
        file = open(name, "r")
        (t, mag, sma) = divide(file)
        data = {'name': maciek, 'date': str(datetime.datetime.now().time()), 'time': t, 'mag': mag, 'sma': sma}
        collection.insert_one(data)
        print("Insert for maciek " + str(i))
    for i in range(1, 11):
        name = stasiu + "/data(" + str(i) + ").txt"
        file = open(name, "r")
        (t, mag, sma) = divide(file)
        data = {'name': stasiu, 'date': str(datetime.datetime.now().time()), 'time': t, 'mag': mag, 'sma': sma}
        collection.insert_one(data)
        print("Insert for stasiu " + str(i))
    for i in range(1, 11):
        name = mrozek + "/data(" + str(i) + ").txt"
        file = open(name, "r")
        (t, mag, sma) = divide(file)
        data = {'name': mrozek, 'date': str(datetime.datetime.now().time()), 'time': t, 'mag': mag, 'sma': sma}
        collection.insert_one(data)
        print("Insert for mrozek " + str(i))

    return 'saveed'


def divide(file):
    t = np.float_(file.readline().replace("t[", "").replace("]", "").replace("\n", "").split(", "))
    mag = np.float_(file.readline().replace("MAG [", "").replace("]", "").replace("\n", "").split(", "))
    sma = np.float_(file.readline().replace("SMA [", "").replace("]", "").split(", "))
    tj = pd.Series(t).to_json(orient='values')
    mj = pd.Series(mag).to_json(orient='values')
    sj = pd.Series(sma).to_json(orient='values')
    return tj, mj, sj
