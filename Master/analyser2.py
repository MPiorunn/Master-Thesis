import matplotlib.pyplot as plt
import numpy as np
from fastdtw import fastdtw
from scipy import signal
import json

friends = ['ania', 'bartek', 'maciek', 'mrozek', 'piorun']

fakes_map = {'ania': 'piorun',
             'piorun': 'mrozek',
             'bartek': 'ania',
             'mrozek': 'piorun',
             'maciek': 'bartek'}


def load_data(path):
    tmp = []
    for i in range(1, 4):
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


data = {}
for friend in friends:
    data[friend] = load_data(friend)
# data['xyz'] = load_data('xyz')
# times = time_analysis(data)
# print(times)
# ania = data['ania'][0]
# ania = data['piorun'][0]
# ania = data['maciek'][0]
# ania = data['mrozek'][0]
# ania = data['bartek'][0]

# signatures = data['ania']
# signatures = data['mrozek']
# signatures = data['maciek']
# signatures = data['bartek']
signatures = data['piorun']
# signatures = data['xyz']

for j in range(2, 3):
    set = signatures[j]
    for i in set:
        t = set[i]['t']
        x = set[i]['sma']
        plt.plot(t, x, marker='o', linestyle='--', color='r')

# for i in range(0, 5):
#     sign = model[str(i)]
#     plt.subplot(5, 1, i + 1)

# sign = model[str(1)]
# plt.plot(sign['t'], sign['y'], 'r', label='y')
# plt.plot(sign['t'], sign['z'], 'y', label='z')
# plt.plot(sign['t'], sign['sma'], 'b', label='sma')
#
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
plt.ylim(0, 2.5)
plt.xlim(0, 5)
plt.legend(loc='upper left')
plt.show()
