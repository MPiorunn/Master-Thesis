import matplotlib.pyplot as plt
import numpy as np
from fastdtw import fastdtw
from scipy import signal
import json

data = []

for i in range(1, 11):
    path = 'Raspberry/signatures/'
    name = path + 'signature(' + str(i) + ').json'
    with open(name) as f:
        file = json.load(f)
        data.append(file)

model = data[0]
sign = model[str(4)]

# for i in range(0, 4):
#     sign = model[str(i)]
#     plt.subplot(5, 1, i + 1)
#
# plt.plot(first['t'], first['x'], 'g', label='x')
# plt.plot(first['t'], first['y'], 'r', label='y')
# plt.plot(first['t'], first['z'], 'y', label='z')
plt.plot(sign['t'], sign['sma'], 'b', label='sma')
plt.legend(loc='upper left')
plt.show()
