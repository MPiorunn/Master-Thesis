import matplotlib.pyplot as plt
import numpy as np
from fastdtw import fastdtw
import scipy
from scipy.stats import pearsonr
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
    fullPath = 'Raspberry/' + path + '/' + path
    name = fullPath + '(' + str(1) + ').json'
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
    global minLen
    averages = []
    for d in someData:
        if len(someData[d]['sma']) > maxLen:
            maxLen = len(someData[d]['sma'])
        if len(someData[d]['sma']) < minLen:
            minLen = len(someData[d]['sma'])

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


def remove_elements_from_end(array, length):
    return array[0:length]


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


def calculate_areas_growth(areas):
    changes = []
    for areaSet in areas:
        sum = areaSet[0]
        growth = []
        for i in range(1, len(areaSet)):
            growth.append(areaSet[i] / sum)
            sum += areaSet[i]
        changes.append(growth)
    return changes


def calculate_dtw(y1, y2):
    distance, path = fastdtw(y1, y2)
    return distance


def calculate_all_dtw(data):
    for i in range(0, len(data)):
        for j in range(0, len(data)):
            if j != i:
                dtw = calculate_dtw(data[i], data[j])
                dtws.append(round(dtw, 4))

    print(dtws)
    dtw_sum = sum(dtws)
    avg_dtw = dtw_sum / len(dtws)
    print('Avg dtw ' + str(avg_dtw))


def autocorelation(signatures):
    time = []
    values = []
    previous_length = 0

    for signature in signatures:
        for t in signatures[signature]['t']:
            time.append(t + previous_length)
        previous_length += signatures[signature]['t'][-1]
        for v in signatures[signature]['sma']:
            values.append(v)
    # np.correlate(first,second)
    return time, values


def calculate_pearsons(data):
    pearson = []
    for i in range(0, len(smas) - 1):
        for j in range(0, len(smas) - 1):
            if i != j:
                first = remove_elements_from_end(data[i], minLen)
                second = remove_elements_from_end(data[j], minLen)
                p, m = pearsonr(first, second)
                pearson.append(p)
    return pearson


# globals
# maximum data pieces in set of charts
global maxLen
maxLen = 0

# shortes dataset
global minLen
minLen = 100000000

# sampling frequency
global freq
freq = 0.025

# into how many parts do we divide each chart?
global chart_divider
chart_divider = 8

data = {}
for friend in friends:
    data[friend] = load_data(friend)

# which friend to check
chart = load_data('ania')[0]
# chart = load_data('piorun')[0]
# chart = load_data('maciek')[0]
# chart = load_data('mrozek')[0]
# zgubiłem dane :(
# chart = load_data('bartek')[0]

# remove outliers or not?
signatures = remove_outliers(chart)
# signatures = chart

# used to group all charts into one dataset

avgs = []
#  sampling frequency
dt = 0.025
plt.subplot(5, 1, 1)
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
    # plt.plot(x, y, marker='o', linestyle='--')
    plt.plot(ts, y, marker='o', linestyle='--')

averageChart = [0] * maxLen

# average values array
for av in avgs:
    for i in range(0, len(av)):
        averageChart[i] += av[i]

# time series
ts = [0] * len(averageChart)
ts[0] = 0
# arrays with upper and lower boundaries
interval = 0.15

# create average chart with boundaries
(upperBorder, lowerBorder) = create_borders(averageChart, interval)

# Calculate coverage for each chart
# divide charts into pieces and calculate area under the chart

averageCoverage = get_signatures_coverage(signatures)

areas = get_signatures_areas(signatures)

changes = calculate_areas_changes(areas)
growth = calculate_areas_growth(areas)
# print charts

# plt.ylim(0, 2.5)
# plt.xlim(0, 2.5)
plt.plot(ts, upperBorder, marker='+', color='r')
plt.plot(ts, averageChart, marker='+', color='b')
plt.plot(ts, lowerBorder, marker='+', color='r')

calculate_dtw(lowerBorder, upperBorder)
plt.subplot(5, 1, 2)

# plot area chanfges
change_x = list(range(1, chart_divider))
for change_y in changes:
    plt.plot(change_x, change_y, marker='o', linestyle='--')

plt.subplot(5, 1, 3)
# plot area growths
growth_x = list(range(1, chart_divider))
for growth_y in growth:
    plt.plot(growth_x, growth_y, marker='o', linestyle='--')

dtws = []

smas = []
for s in signatures:
    smas.append(signatures[s]['sma'])

pearson = []
for i in range(0, len(smas) - 1):
    for j in range(0, len(smas) - 1):
        if i != j:
            first = remove_elements_from_end(smas[i], minLen)
            second = remove_elements_from_end(smas[j], minLen)
            p, m = pearsonr(first, second)
            pearson.append(p)

print("Avg:")
print(statistics.mean(pearson))
print("Median:")
print(statistics.median(pearson))

print("SMA dtws")
calculate_all_dtw(smas)

print("Changes DTWs")
calculate_all_dtw(changes)

print("Growth DTWs")
calculate_all_dtw(growth)

print("Pearsons")
prsn = calculate_pearsons(smas)
print(prsn)
print("Average pearson")
print(np.mean(prsn))



(time, values) = autocorelation(signatures)
plt.subplot(5, 1, 4)
plt.plot(time, values)

plt.subplot(5, 1, 5)
plt.acorr(values)

# plt.legend(loc='upper left')
plt.show()
