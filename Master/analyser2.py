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


def create_borders(base, interval):
    upperBorder = [0] * len(base)
    lowerBorder = [0] * len(base)
    for i in range(1, len(base)):
        base[i] /= chart_divider
        upperBorder[i] = base[i] + interval
        lowerBorder[i] = base[i] - interval
        ts[i] = ts[i - 1] + freq
    return upperBorder, lowerBorder


def get_signatures_areas(signatures):
    areas = []
    for i in signatures:
        y = signatures[str(i)]['sma']
        area = calculate_area_intervals(y, freq, chart_divider)
        areas.append(area)
    return areas


def get_signatures_coverage(signatures):
    avg = 0
    for i in signatures:
        y = signatures[str(i)]['sma']
        coverage = chart_coverage(y, upperBorder, lowerBorder)
        avg += coverage
    return avg / chart_divider


def calculate_areas_changes(areas):
    changes = []
    for areaSet in areas:
        sign_changes = []
        for i in range(1, len(areaSet)):
            sign_changes.append(areaSet[i] / areaSet[i - 1])
        changes.append(sign_changes)
    return changes


# globals
# maximum data pieces in set of charts
global maxLen
maxLen = 0

# sampling frequency
global freq
freq = 0.025

# into how many parts do we divide each chart?
global chart_divider
chart_divider = 8

data = {}
# for friend in friends:
# data[friend] = load_data(friend)
# data['xyz'] = load_data('xyz')
data['ania'] = load_data('ania')
# times = time_analysis(data)
# print(times)
# which friend to check
chart = data['ania'][0]
# chart = data['piorun'][0]
# chart = data['maciek'][0]
# chart = data['mrozek'][0]
# chart = data['bartek'][0]

# remove outliers or not?
signatures = remove_outliers(chart)
# signatures = chart

# used to group all charts into one dataset

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
    avgs.append(avg)
    # plt.plot(x, y, marker='o', linestyle='--', color='r')
    # plt.plot(ts, y, marker='o', linestyle='--', color='r')

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

# create average chart with boundaries
(upperBorder, lowerBorder) = create_borders(averageChart, interval)

# Calculate coverage for each chart
# divide charts into pieces and calculate area under the chart

averageCoverage = get_signatures_coverage(signatures)

areas = get_signatures_areas(signatures)

changes = calculate_areas_changes(areas)
# print charts

# plt.plot(ts, upperBorder, marker='o', linestyle='--', color='y')
# plt.plot(ts, averageChart, marker='o', linestyle='--', color='b')
# plt.plot(ts, lowerBorder, marker='o', linestyle='--', color='g')
change_x = list(range(1, chart_divider))
for change_y in changes:
    plt.plot(change_x, change_y, marker='o', linestyle='--')

# plt.ylim(0, 2.5)
# plt.xlim(0, 2.5)
plt.legend(loc='upper left')
plt.show()
