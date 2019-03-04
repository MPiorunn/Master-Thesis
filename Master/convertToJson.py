import json
import numpy as np


def readFile(path):
    with open(path + 'txt', "r") as file:
        t = file.readline().replace("t[", "").replace("]", "").replace("\n", "").split(", ")
        mag = file.readline().replace("MAG [", "").replace("]", "").replace("\n", "").split(", ")
        sma = file.readline().replace("SMA [", "").replace("]", "").split(", ")

    with open(path + 'json', "w+") as outfile:
        jsone = {'t': t, 'mag': mag, 'sma': sma}
        json.dump(jsone, outfile)


for i in range(1, 11):
    p = 'stasiu/data(' + str(i) + ').'
    readFile(p)

for i in range(1, 11):
    p = 'mrozek/data(' + str(i) + ').'
    readFile(p)

for i in range(1, 6):
    p = 'ja/data' + str(i) + '.'
    readFile(p)
