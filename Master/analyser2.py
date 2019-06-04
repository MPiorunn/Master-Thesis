import matplotlib.pyplot as plt
import numpy as np
from fastdtw import fastdtw
import scipy
from scipy.stats import pearsonr
import json
import math
import statistics
from pandas.io.json import json_normalize

friends = ['ania', 'bartek', 'maciek', 'mrozek', 'piorun', 'przemek', 'my']


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
        if d not in ['10', '12']:
            averages.append(statistics.mean(someData[d]['sma']))
    minI = averages.index(min(averages))
    maxI = averages.index(max(averages))
    someData.pop(str(minI))
    someData.pop(str(maxI))
    for d in someData:
        if len(someData[d]['sma']) > maxLen:
            maxLen = len(someData[d]['sma'])
        if len(someData[d]['sma']) < minLen:
            minLen = len(someData[d]['sma'])
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


def create_borders(base, interval, dividers):
    upperBorder = [0] * len(base)
    lowerBorder = [0] * len(base)
    for i in range(1, len(base)):
        if dividers[i] != 0:
            base[i] /= dividers[i]
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
        signatures[signature]['t'] = remove_elements_from_end(signatures[signature]['t'], minLen)
        signatures[signature]['sma'] = remove_elements_from_end(signatures[signature]['sma'], minLen)
        for t in signatures[signature]['t']:
            time.append(t + previous_length)
        previous_length += signatures[signature]['t'][-1]
        for v in signatures[signature]['sma']:
            values.append(v)
    return time, values


def calculate_pearsons(data, average):
    pearson = []
    for i in range(0, len(data)):
        p, m = pearsonr(data[i], average)
        pearson.append(p)
        #     for j in range(0, len(smas) - 1):
        #         if i != j:
        #             first = remove_elements_from_end(data[i], minLen)
        #             second = remove_elements_from_end(data[j], minLen)
    return pearson


def calculate_dtw_with_average(data, average):
    tmp = []
    for d in data:
        tmp.append(calculate_dtw(d, average))
    print('DTWs with average chart')
    print(tmp)
    print('Average dtw')
    print(np.mean(tmp))


def load_data(path):
    tmp = []
    tmp2 = []
    fullPath = 'Raspberry/' + path + '/' + path
    name = fullPath + '(' + str(1) + ').json'
    with open(name) as f:
        tmp.append(json.load(f))

    name = fullPath + '(' + str(3) + ').json'
    with open(name) as f:
        tmp2.append(json.load(f))
    tmp[0]['10'] = tmp2[0]['0']
    tmp[0]['12'] = tmp2[0]['1']
    # tmp[0]['13'] = tmp2[0]['2']
    # tmp[0]['14'] = tmp2[0]['3']
    # tmp[0]['15'] = tmp2[0]['4']
    return tmp


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

std_dev = []
variances = []
data = {}
# for friend in friends:
#     data[friend] = load_data(friend)

# which friend to check
# chart = load_data('przemek')[0]
# chart = load_data('ania')[0]
# chart = load_data('piorun')[0]
# chart = load_data('maciek')[0]
chart = load_data('mrozek')[0]
# chart = load_data('my')[0]

# remove outliers or not?
signatures = remove_outliers(chart)
# signatures = chart

# used to group all charts into one dataset

avgs = []
#  sampling frequency
dt = 0.025
# plt.subplot(5, 1, 1)
plt.figure()
for i in signatures:
    x = signatures[str(i)]['t']
    y = signatures[str(i)]['sma']
    d = signatures[str(i)]['x']
    b = signatures[str(i)]['y']
    c = signatures[str(i)]['z']
    t = 0.0
    ts = []
    mag = []
    avg = [0] * maxLen
    for a in range(0, len(x)):
        ts.append(t)
        t = round((t + dt), 3)
        avg[a] = y[a]
        mag.append(math.sqrt((d[a] * d[a]) + (b[a] * b[a]) + (c[a] * c[a])))
    avgs.append(avg)
    # if i == '0':
    # plt.plot(x, mag)
    # plt.plot(x, y)
    # variances.append(np.var(y))
    # std_dev.append(np.std(y))
    if int(i) < 10:
        plt.plot(ts, y, marker='o', linestyle='--', color='r')
    else:
        plt.plot(ts, y, marker='o', linestyle='--', color='b')

plt.xlabel('Time', fontsize=18)
plt.ylabel('Acceleration', fontsize=18)
averageChart = [0] * maxLen

# average values array
dividers = [0] * len(averageChart)
# tutaj trzeba zakomentować, bo do średniego przebiegu bierze falsyfikaty, trzeba wartość ustawić na sztywno, tyle ile mamy origynałów
# for av in avgs:
for j in range(0, 8):
    for i in range(0, len(avgs[j])):
        if avgs[j][i] > 0:
            dividers[i] += 1
        averageChart[i] += avgs[j][i]

# time series
ts = [0] * len(averageChart)
ts[0] = 0
# arrays with upper and lower boundaries
interval = 0.15

# create average chart with boundaries
(upperBorder, lowerBorder) = create_borders(averageChart, interval, dividers)

# Calculate coverage for each chart
# divide charts into pieces and calculate area under the chart

# averageCoverage = get_signatures_coverage(signatures)

areas = get_signatures_areas(signatures)

changes = calculate_areas_changes(areas)
growth = calculate_areas_growth(areas)
# print charts
# AVERAGE CHART CHANGE

sums = [0] * (chart_divider - 1)

for j in range(0, 5):
    for i in range(0, (chart_divider - 1)):
        sums[i] += changes[j][i] / 5

plt.ylim(0, 2)
# plt.xlim(0, 3.5)
# plt.plot(ts, upperBorder, marker='+', color='g')
# plt.plot(ts, averageChart, marker='o', color='g', linewidth=4)
# plt.plot(ts, lowerBorder, marker='+', color='g')

calculate_dtw(lowerBorder, upperBorder)
# plt.subplot(5, 1, 2)
# plt.figure()

# plot area chanfges
# change_x = list(range(1, chart_divider))
# for i in range(0, len(changes)):
#     if i < 8:
#         plt.plot(change_x, changes[i], marker='o', linestyle='--', color='r')
#     else:
#         plt.plot(change_x, changes[i], marker='o', linestyle='--', color='b')
# plt.plot(change_x, sums, marker='o', color='g', linewidth='4')
# plt.subplot(5, 1, 3)
# plt.figure()
# plot area growths
growth_x = list(range(1, chart_divider))
# for growth_y in growth:
#     plt.plot(growth_x, growth_y, marker='o', linestyle='--')

dtws = []

smas = []
for s in signatures:
    smas.append(signatures[s]['sma'][:minLen])

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

print("SMA with average chart")
calculate_dtw_with_average(smas, averageChart)

corrects = []
coefficient = 0.3
for j in range(0, len(changes)):
    correct = [0] * chart_divider
    for i in range(0, len(changes[j])):
        # print(str(j) + ' : ' + str(i))
        # print("Comparing " + str(sums[i] * (1 - coefficient)) + " With " + str(changes[j][i]) + " and " + str(
        #     sums[i] * (1 + coefficient)))
        if (changes[j][i] * (1 - coefficient)) < sums[i] < (changes[j][i] * (1 + coefficient)):
            correct[i] = 1
    corrects.append(correct)

print("Changes DTWs")
print(changes)
calculate_all_dtw(changes)

print("Growth DTWs")
print(growth)
calculate_all_dtw(growth)

print("Pearsons")
# prsn = calculate_pearsons(smas, averageChart)
# print(prsn)

# print("Average pearson")
# print(np.mean(prsn))

(time, values) = autocorelation(signatures)
# plt.subplot(5, 1, 4)
# plt.figure()
# plt.plot(time, values)

# plt.subplot(5, 1, 5)
# plt.figure()
# plt.acorr(values, maxlags=80)
#
# for i in range(0, len(corrects)):
#     print(changes[i])
#     print(corrects[i])
#     procent = 0
#     for a in corrects[i]:
#         if a == 1:
#             procent += 1
#     print(procent / len(corrects[i]))

# plt.legend(loc='upper left')

# wariacje i odchylenia do pokazania że usuwanie ooutlierów działa

# print('avg std')
# print(np.average(std_dev))

# print('avg var')
# print(np.average(variances))

print('avg chart std')
print(np.std(averageChart))

print('avg chart var')
print(np.var(averageChart))

# obliczenie dtw między średnim przebiegiem a całą resztą
calculated_dtws = []
tmp_avg_chart = [0.0, 0.06244352672515947, 0.1988224830217309, 0.3401440037634977, 0.4424202581671502,
                 0.4823738801350672, 0.5112105906608775, 0.5587799794185058, 0.627264139218095, 0.7288276001680144,
                 0.7968782739446141, 0.8262724108842474, 0.8363947020220481, 0.850116256463306, 0.8769204044522563,
                 0.8780451100989871, 0.8937425453207115, 0.8541009981450409, 0.8585667485769033, 0.8211382456935039,
                 0.8427265639840281, 0.8417341972756969, 0.8160028778744662, 0.8292686142211679, 0.8034598453545878,
                 0.8155743761804692, 0.7474261760451074, 0.7532998842717346, 0.7203314450046555, 0.7239720849953533,
                 0.6539758946967014, 0.6490699814032891, 0.6301666954365264, 0.5981154781287157, 0.5862528724963708,
                 0.5362814036059166, 0.5470480909625997, 0.5219639171104633, 0.4805186686397085, 0.4531774904628806,
                 0.4285131983679099, 0.4396496681347913, 0.4176922910985796, 0.4318414959705112, 0.3299434452911785,
                 0.33404603223615387, 0.3326054858720589, 0.3106091803346822, 0.2668736598078695, 0.33720105004758877,
                 0.39627697775223436, 0.3827962269697715, 0.3870861839360872]
# for sma in smas:
#     calculated_dtws.append(calculate_dtw(sma, averageChart))
# print("average dtw")
# average_distance = np.average(calculated_dtws)
# print(average_distance)
# print("20%")
# print(average_distance * 0.8)
# print(average_distance * 1.2)
# print("40%")
# print(average_distance * 0.6)
# print(average_distance * 1.4)
# print("60%")
# print(average_distance * 0.4)
# print(average_distance * 1.6)

# print(calculated_dtws)
# plt.plot(ts[:53], tmp_avg_chart, marker='o', color='g', linewidth=3)
# plt.show()

list = [0.9686437079483431, 0.9483549999774922, 0.9747874034194368, 0.985958324098727, 0.7814346960103109, 0.9201161138348891, 0.9578736357202665, 0.9670556383306563]
print(np.average(list))

