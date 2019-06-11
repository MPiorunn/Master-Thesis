import matplotlib.pyplot as plt
import numpy as np
from fastdtw import fastdtw
import scipy
from scipy.stats import pearsonr
from scipy import signal
import json
import math
import statistics
from pandas.io.json import json_normalize


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
        if d not in ['10', '12', '13', '14', '15']:
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

    # print(dtws)
    dtw_sum = sum(dtws)
    avg_dtw = dtw_sum / len(dtws)
    # print('Avg dtw ' + str(avg_dtw))


def autocorelation(t, sma, t_avg, sma_avg):
    time = []
    tt = t
    # tt = remove_elements_from_end(t, minLen)
    # smaa = remove_elements_from_end(sma, minLen)

    for t in t_avg:
        time.append(t)
    last = time[-1]
    for t in tt:
        time.append(t + last)
    return time, sma_avg + sma


def calculate_pearsons(data, average):
    pearson = []
    for i in range(0, len(data)):
        p, m = pearsonr(data[i][:minLen], average[:minLen])
        pearson.append(p)
    return pearson


def calculate_dtw_with_average(data, average):
    tmp = []
    for d in data:
        tmp.append(calculate_dtw(d, average))
    # print('DTWs with average chart')
    # print(tmp)
    # print('Average dtw')
    # print(np.mean(tmp))


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
    tmp[0]['13'] = tmp2[0]['2']
    tmp[0]['14'] = tmp2[0]['3']
    tmp[0]['15'] = tmp2[0]['4']
    return tmp


def calculate_far_frr(fp, fn, tn, tp):
    far = fp / (fp + tn)
    frr = fn / (fn + tp)
    return far, frr


def calculate_far_frr_from_results(results):
    good_amount = 8
    bad_amount = 5
    fp, fn, tn, tp = 0, 0, 0, 0
    for i in range(0, good_amount):
        if results[i]:
            tp += 1
        else:
            tn += 1
        print(i)
    for i in range(good_amount, bad_amount + good_amount - 1):
        if results[i]:
            fp += 1
        else:
            fn += 1
        print(i)
    return calculate_far_frr(fp, fn, tn, tp)


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

# which friend to check
# chart = load_data('przemek')[0]
chart = load_data('ania')[0]
# chart = load_data('piorun')[0]
# chart = load_data('maciek')[0]
# chart = load_data('mrozek')[0]
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
# print(averageChart)

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

# plt.ylim(0, 1.5)
# plt.xlim(0, 3.5)
# plt.plot(ts, upperBorder, marker='+', color='g')

# mrozek
# tmp = [0.0, 0.06244352672515947, 0.1988224830217309, 0.3401440037634977, 0.4424202581671502, 0.4823738801350672,
#        0.5112105906608775, 0.5587799794185058, 0.627264139218095, 0.7288276001680144, 0.7968782739446141,
#        0.8262724108842474, 0.8363947020220481, 0.850116256463306, 0.8769204044522563, 0.8780451100989871,
#        0.8937425453207115, 0.8541009981450409, 0.8585667485769033, 0.8211382456935039, 0.8427265639840281,
#        0.8417341972756969, 0.8160028778744662, 0.8292686142211679, 0.8034598453545878, 0.8155743761804692,
#        0.7474261760451074, 0.7532998842717346, 0.7203314450046555, 0.7239720849953533, 0.6539758946967014,
#        0.6490699814032891, 0.6301666954365264, 0.5981154781287157, 0.5862528724963708, 0.5362814036059166,
#        0.5470480909625997, 0.5219639171104633, 0.4805186686397085, 0.4531774904628806, 0.4285131983679099,
#        0.4396496681347913, 0.4176922910985796, 0.4318414959705112, 0.3299434452911785, 0.33404603223615387,
#        0.3326054858720589, 0.3106091803346822, 0.2668736598078695, 0.33720105004758877, 0.39627697775223436,
#        0.3827962269697715, 0.3870861839360872]
# ania
tmp = [0.0, 0.04700538449949179, 0.1277341055276281, 0.24852709338981877, 0.35160879797008765, 0.43776990871518623,
       0.5038210900097466, 0.5514654853784549, 0.6203049553414841, 0.6750338386758821, 0.7224589374131908,
       0.7381873872895583, 0.7608722368918905, 0.79268605731764, 0.8047993087075109, 0.8232334150100311,
       0.8274526187112863, 0.8358728955370592, 0.8241741840958878, 0.8242966087307637, 0.814520276324839,
       0.7952531262420509, 0.7909390503698763, 0.7828096680342987, 0.7825212071322811, 0.7609306095377272,
       0.74990946328382, 0.7042399830047262, 0.6733639331539177, 0.661128642465668, 0.6595760438844578,
       0.6359340947975884, 0.5867513733618913, 0.5621992607000167, 0.5259150236445759, 0.4997438311218923,
       0.4754650500451445, 0.4476184908971858, 0.43567715420259134, 0.4180700077413659, 0.4082088856047738,
       0.41002710826302746, 0.4009101446711465, 0.3736317756895499, 0.37585063298189164, 0.39179382571464944,
       0.4089966515449967, 0.42714900743192796, 0.4342707055405118, 0.42053836928619465, 0.4334612177616712,
       0.5027396706005045, 0.4569690650297926, 0.36060416413231783, 0.22808220718674022, 0.2642586168501419,
       0.2601850872715106, 0.1943217787356767]
# maciek
# tmp = [0.0, 0.029338830508917724, 0.05281555446164198, 0.09736067250943567, 0.12077268369268544, 0.1392357065230654,
#        0.13886746661962826, 0.15556887699084382, 0.2027627140683661, 0.2229293102555548, 0.22773215070068126,
#        0.21643681482566632, 0.2542406470038146, 0.27461616528499555, 0.30213909890259516, 0.3236381720974132,
#        0.31202563787630366, 0.29189821694109896, 0.26354383623567756, 0.2604288782849482, 0.25844900554022837,
#        0.2501278776639491, 0.24192344866387097, 0.23319584409212318, 0.21359110973299614, 0.215400528592088,
#        0.20797301351554198, 0.21282721073958127, 0.20140732615406204, 0.22192288400193572, 0.22372173809194676,
#        0.22703839366326914, 0.20289844934467421, 0.19920909044646087, 0.20169762497132626, 0.20180565577389514,
#        0.21108089413650094, 0.2064286491983011, 0.2201428587047081, 0.21286907852219672, 0.2207947124270762,
#        0.21670378979172564, 0.23648785751496046, 0.25696451657052083, 0.2567253079842166, 0.2309273777982376,
#        0.2286500478214674, 0.23149562827443876, 0.2425363947385211, 0.2059810390747646, 0.18241627255878642,
#        0.16450514423444473, 0.1678053493872564, 0.18256868623445618, 0.22669314984454147, 0.21459128679032208,
#        0.21983295790560886, 0.19334201033337486, 0.22795008642867584, 0.2175629953649556, 0.20658491400397133,
#        0.18490488612016923, 0.1863279803178886, 0.19284014419889317, 0.2063310888465079, 0.21050510783738463,
#        0.19816206434439332, 0.20364853635155208, 0.2526068870757532, 0.25795216470060084, 0.2507967262990478,
#        0.20285349116532392, 0.19811245368779, 0.22334000306690027, 0.23990031493562952, 0.26556381669896645,
#        0.2433468999505115, 0.28952643456177984, 0.27666397237797263, 0.26537158552410417, 0.19387336856620982,
#        0.18165459146388457, 0.2219315100901611, 0.22211606021774316, 0.2353323475543262, 0.1995704604891021,
#        0.19481670214340763, 0.19210704743620385, 0.1899977754738668, 0.18492383196902598, 0.20057329604718493,
#        0.21712431354872594, 0.23338925331600616, 0.2088493806559157, 0.19037551856237894, 0.16961163542075366,
#        0.18069560755732098, 0.20334607646692773, 0.22063655322014364, 0.24208753881230258, 0.255189569189987,
#        0.2591894268005301, 0.2683176292434794, 0.3161450706753196, 0.43526981166884404, 0.39929134396138943,
#        0.3982302865030839, 0.4415715142382383, 0.5680618354997179, 0.514963521537717, 0.6087217100229165,
#        0.38707828649125503, 0.5611224556212854, 0.5870901670012872, 0.4637011926180217, 0.24094143701474313]
# przemek
# tmp = [0.0, 0.04085334202536968, 0.09338030823603952, 0.14532353987833263, 0.1733395066463119, 0.25585714998878595,
#        0.29799762936688673, 0.3499886673750415, 0.3464547429130949, 0.367242617321491, 0.36317639986322287,
#        0.37593296508240986, 0.41884432044791303, 0.437610883089645, 0.40299193125207, 0.4306104005954152,
#        0.4104004417382385, 0.410565239839966, 0.347734900360127, 0.36795758044136373, 0.36835602628324443,
#        0.36075607489423794, 0.33489527313580003, 0.3410813157610525, 0.3335093726947406, 0.31618585792495774,
#        0.3124550009274826, 0.30120401005361286, 0.3083308944088691, 0.28889263436515283, 0.2742841942689509,
#        0.25228212912866127, 0.2495591424887322, 0.2535407538759473, 0.24984661116768955, 0.23849462315057182,
#        0.2551599248027225, 0.25255552688766525, 0.23667994501940737, 0.21184730627071038, 0.2274922276176208,
#        0.24262975331588196, 0.2341533566223835, 0.22090386909173665, 0.21394056210167206, 0.2184178561381195,
#        0.19775103570504615, 0.1902154341068641, 0.21654705704185742, 0.24443371917620324, 0.2381263736321323,
#        0.20593594541496077, 0.23828072559235391, 0.2501096991753595, 0.2659059796056051, 0.23838719704974984,
#        0.25574124527253217, 0.25063218979359764, 0.21046057786804523, 0.18055277547299803, 0.16591294058042055,
#        0.18113944491674824, 0.18510874982811482, 0.18049714150544371, 0.18324102289850486, 0.17379838990368773,
#        0.1899649210815284, 0.18001582765544893, 0.17158843669212873, 0.15573151927522705, 0.16282763594999236,
#        0.16148902444423913, 0.1763760166567651, 0.16333081590533519, 0.16031407080500207, 0.15356504449199385,
#        0.15750277609568966, 0.17941343138487298, 0.1806224446802631, 0.17233439021960917, 0.16743731160049088,
#        0.1984051833888296, 0.21297893138086557, 0.2413790327069132, 0.16870811827294824, 0.27732670020646716,
#        0.39956168753117444]
plt.plot(ts[:len(tmp)], tmp, marker='o', color='g', linewidth=4)
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
# growth_x = list(range(1, chart_divider))
# for growth_y in growth:
#     plt.plot(growth_x, growth_y, marker='o', linestyle='--')


print()
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

# print("Changes DTWs")
# print(changes)
# calculate_all_dtw(changes)

# print("Growth DTWs")
# print(growth)
# calculate_all_dtw(growth)

print("Pearsons")
prsn = calculate_pearsons(smas, tmp)
print(prsn)

print("Average pearson")
print(np.mean(prsn))
print()
print()
print()
print()
# (time, values) = autocorelation(signatures['1']['t'], signatures['1']['sma'], ts[:len(tmp)], tmp)
print("AUTOKORELACJA")
# for s in signatures:
#     (time, values) = autocorelation(signatures[s]['t'], signatures[s]['sma'], ts[:len(tmp)], tmp)
#     plt.figure()
#     plt.subplot(2, 1, 1)
#     plt.xlabel('Time', fontsize=18)
#     plt.ylabel('Acceleration', fontsize=18)
#     plt.plot(time[:len(tmp)], values[:len(tmp)], color='g')
#     plt.plot(time[len(tmp):], values[len(tmp):], color='b')
#     plt.subplot(2, 1, 2)
#     plt.ylabel('Correlation', fontsize=18)
#     plt.xlabel('Lag', fontsize=18)
#     a = plt.acorr(values, maxlags=80)
#     correclation = a[1].tolist()[120:]
#     peaks = signal.find_peaks(correclation, height=0)
#     max = 0
#     if len(peaks[1]['peak_heights'].tolist()):
#         max = peaks[1]['peak_heights'].tolist()[-1]
#     print(max)
#     plt.title(max)
#     for i in range(0, len(correclation) - 1):
#         if correclation[i] < correclation[i + 1]:
#             print(i)
#             diff = correclation[i] - correclation[i + 1]
#             print(diff)
#             print()
#             break
print()
print()
print()
print()
print()

# obliczenie dtw między średnim przebiegiem a całą resztą
print("SMA")
calculated_dtws = []
for sma in smas:
    calculated_dtws.append(calculate_dtw(sma, tmp))
print("average dtw")
average_distance = np.average(calculated_dtws)
print(average_distance)
print("20%")
print(average_distance * 0.8)
print(average_distance * 1.2)
print("40%")
print(average_distance * 0.6)
print(average_distance * 1.4)
print("60%")
print(average_distance * 0.4)
print(average_distance * 1.6)

print(calculated_dtws)

print()
print()
print()
print()
print()

print("AREA CHANGES : ")
average_changes = [0] * (chart_divider - 1)
for gru in growth:
    print(gru)
    for i in range(0, (chart_divider - 1)):
        average_changes[i] += gru[i] / len(smas)

print("AVERAGE CHANGES")
print(average_changes)

results = []
for gru in growth:
    passed = 0

    for i in range(0, chart_divider - 1):
        if average_changes[i] * 0.7 < gru[i] < average_changes[i] * 1.3:
            passed += 1
    result = math.fabs(passed / chart_divider)
    print(result)
    results.append(result > 0.73)
far, frr = calculate_far_frr_from_results(results)
print("FAR")
print(far)

print("FRR")
print(frr)
# todo podrobić podpisy przemka, dorobić kilka swoich,, żeby było 10, jest 5
plt.show()
