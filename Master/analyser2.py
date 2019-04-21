import matplotlib.pyplot as plt
import numpy as np
from fastdtw import fastdtw
import scipy
import json
import math
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


def calculate_area(y, dx):
    return scipy.trapz(y, dx=dx)


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def calculate_area_intervals(y, dx, intervals):
    chunks = list(split(y, intervals))
    areas = []
    for chunk in chunks:
        areas.append(calculate_area(chunk, dx))
    return areas


def chart_coverage(fx, up, down):
    matched = 0
    for i in range(0, len(fx)):
        if up[i] >= fx[i] >= down[i]:
            matched += 1
    return matched / len(fx)


data = {}
for friend in friends:
    data[friend] = load_data(friend)
# data['xyz'] = load_data('xyz')
# times = time_analysis(data)
# print(times)
maxLen = 0

# which friend to check
# chart = data['ania'][0]
# chart = data['piorun'][0]
# chart = data['maciek'][0]
chart = data['mrozek'][0]
# chart = data['bartek'][0]

# remove outliers or not?
signatures = remove_outliers(chart)
# signatures = chart

# used to group all charts into one dataset
# results = {'pairs': []}

avgs = []
#  sampling frequency
dt = 0.025
for i in signatures:
    x = signatures[str(i)]['t']
    y = signatures[str(i)]['sma']
    t = 0.0
    ts = []
    avg = [0] * maxLen
    for a in range(0, len(x)):
        ts.append(t)
        t = round((t + dt), 3)
        avg[a] = y[a]
        # results['pairs'].append({'x': t, 'y': y[a]})
        # results['pairs'].append({'x': x[a], 'y': y[a]})
    avgs.append(avg)
    # plt.plot(x, y, marker='o', linestyle='--', color='r')
    plt.plot(ts, y, marker='o', linestyle='--', color='r')

averageChart = [0] * maxLen

# average values array
for av in avgs:
    for i in range(0, len(av)):
        averageChart[i] += av[i]

# time series
ts = [0] * len(averageChart)
ts[0] = 0
# arrays with upper and lower boundaries
interval = 0.1
upperBorder = [0] * len(averageChart)
lowerBorder = [0] * len(averageChart)
# create average chart with boundaries
for i in range(1, len(averageChart)):
    averageChart[i] /= 8
    upperBorder[i] = averageChart[i] + interval
    lowerBorder[i] = averageChart[i] - interval
    ts[i] = ts[i - 1] + 0.025

# Calculate coverage for each chart
averageCoverage = 0

for i in signatures:
    y = signatures[str(i)]['sma']
    coverage = chart_coverage(y, upperBorder, lowerBorder)
    print("Coverage : " + str(coverage))
    print("Areas : " + str(calculate_area_intervals(y, 0.025, 8)))
    averageCoverage += coverage

averageCoverage /= 8
print("Average coverage : " + str(averageCoverage))

# divide charts into pieces and calculate area under the chart
# print charts

plt.plot(ts, upperBorder, marker='o', linestyle='--', color='y')
plt.plot(ts, averageChart, marker='o', linestyle='--', color='b')
plt.plot(ts, lowerBorder, marker='o', linestyle='--', color='g')

# sorted(results['pairs'], key=lambda i: i['x'])

# xval = []
# yval = []
# for result in results:
#     xval.append(result)
#     yval.append(results[result])

# xy = []
# yy = []
# for res in results['pairs']:
#     xy.append(res['x'])
#     yy.append(res['y'])
plt.ylim(0, 2.5)
plt.xlim(0, 2.5)
plt.legend(loc='upper left')
plt.show()
