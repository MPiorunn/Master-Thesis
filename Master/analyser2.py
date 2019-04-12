import matplotlib.pyplot as plt
import numpy as np
from fastdtw import fastdtw
from scipy import signal
import json

data = []

for i in range(1, 11):
    path = 'Raspberry/xyz/'
    name = path + 'xyz(' + str(i) + ').json'
    with open(name) as f:
        file = json.load(f)
        data.append(file)

model = data[1]
first = model[str(1)]

plt.plot(first['t'], first['x'], 'g', label='x')
plt.plot(first['t'], first['y'], 'r', label='y')
plt.plot(first['t'], first['z'], 'y', label='z')
plt.plot(first['t'], first['sma'], 'b', label='sma')
plt.legend(loc='upper left')
plt.show()
