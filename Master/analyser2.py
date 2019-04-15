import matplotlib.pyplot as plt
import numpy as np
from fastdtw import fastdtw
from scipy import signal
import json

friends = ['ania', 'bartek', 'maciek', 'mrozek', 'piorun']


def load_data(path):
    tmp = []
    for i in range(1, 4):
        fullPath = 'Raspberry/' + path + '/' + path
        name = fullPath + '(' + str(i) + ').json'
        with open(name) as f:
            tmp.append(json.load(f))
    return tmp


def time_analysis(datasets):
    for dataset in datasets:
        print()
        for file in dataset:
            print()
            for signature in file:
                l = len(file[signature]['t'])
                print(file[signature]['t'][l - 1])


data = []
for friend in friends:
    data.append(load_data(friend))

time_analysis(data)
# for i in range(0, 5):
#     sign = model[str(i)]
#     plt.subplot(5, 1, i + 1)

# sign = model[str(1)]
# plt.plot(sign['t'], sign['x'], 'g', label='x')
# plt.plot(sign['t'], sign['y'], 'r', label='y')
# plt.plot(sign['t'], sign['z'], 'y', label='z')
# plt.plot(sign['t'], sign['sma'], 'b', label='sma')
#
# plt.legend(loc='upper left')
# plt.show()
#
