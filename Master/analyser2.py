import matplotlib.pyplot as plt
import numpy as np
from fastdtw import fastdtw
from scipy import signal
import json
import statistics
from pandas.io.json import json_normalize

friends = ['ania', 'bartek', 'maciek', 'mrozek', 'piorun']

fakes_map = {'ania': 'piorun',
             'piorun': 'mrozek',
             'bartek': 'ania',
             'mrozek': 'piorun',
             'maciek': 'bartek'}


def load_data(path):
    tmp = []
    for i in range(1, 2):
        fullPath = 'Raspberry/' + path + '/' + path
        name = fullPath + '(' + str(i) + ').json'
        with open(name) as f:
            tmp.append(json.load(f))
    return tmp


def time_analysis(datasets):
    tmp = []
    for dataset in datasets:
        for file in dataset:
            for signature in file:
                for name in signature:
                    l = len(file[name]['t'])
                    tmp.append(file[name]['t'][l - 1])
    return tmp


def remove_outliers(someData):
    global maxLen
    averages = []
    for d in someData:
        if len(someData[d]['sma']) > maxLen:
            maxLen = len(someData[d]['sma'])
        averages.append(statistics.mean(someData[d]['sma']))
    minI = averages.index(min(averages))
    maxI = averages.index(max(averages))
    someData.pop(str(minI))
    someData.pop(str(maxI))
    # print('Removed min : ' + str(minI) + ' and max : ' + str(maxI))
    return someData


data = {}
for friend in friends:
    data[friend] = load_data(friend)
# data['xyz'] = load_data('xyz')
# times = time_analysis(data)
# print(times)
maxLen = 0

# which friend to check
# ania = data['ania'][0]
# ania = data['piorun'][0]
# ania = data['maciek'][0]
chart = data['mrozek'][0]
# ania = data['bartek'][0]

# remove outliers or not?
signatures = remove_outliers(chart)
# signatures = ania

# used to group all charts into one dataset
results = {'pairs': []}

avgs = []
for i in signatures:
    x = signatures[str(i)]['t']
    y = signatures[str(i)]['sma']
    t = 0.0
    #  kontrola czestosci probkowania
    ts = []
    avg = [0] * maxLen
    # znalezienie usrednionego wykresu zeby zrobic tasme
    for a in range(0, len(x)):
        ts.append(t)
        results['pairs'].append({'x': t, 'y': y[a]})
        t = round((t + 0.025), 3)
        avg[a] = y[a]
        # results['pairs'].append({'x': x[a], 'y': y[a]})
    avgs.append(avg)
    # plt.plot(x, y, marker='o', linestyle='--', color='r')
    plt.plot(ts, y, marker='o', linestyle='--', color='r')

averageChart = [0] * maxLen
# for av in avgs:

xval = []
yval = []
# stworzenie tablicy z srednimi wartosciami
for av in avgs:
    for i in range(0, len(av)):
        averageChart[i] += av[i]

ts = [0] * len(averageChart)
ts[0] = 0
interval = 0.1
upperBorder = [0] * len(averageChart)
lowerBorder = [0] * len(averageChart)
for i in range(0, len(averageChart)):
    averageChart[i] /= 8
    upperBorder[i] = averageChart[i] + interval
    lowerBorder[i] = averageChart[i] - interval
    if i > 0:
        ts[i] = ts[i - 1] + 0.025

for result in results:
    xval.append(result)
    yval.append(results[result])

plt.plot(ts, upperBorder, marker='o', linestyle='--', color='y')
plt.plot(ts, averageChart, marker='o', linestyle='--', color='b')
plt.plot(ts, lowerBorder, marker='o', linestyle='--', color='g')
# Sort all points by time. Does not affect the chart
sorted(results['pairs'], key=lambda i: i['x'])

xy = []
yy = []
for res in results['pairs']:
    xy.append(res['x'])
    yy.append(res['y'])
plt.ylim(0, 2.5)
plt.xlim(0, 2.5)
plt.legend(loc='upper left')
plt.show()

