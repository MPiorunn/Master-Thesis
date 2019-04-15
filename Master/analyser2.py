import matplotlib.pyplot as plt
import numpy as np
from fastdtw import fastdtw
from scipy import signal
import json

data = []

for i in range(1, 8):
    path = 'Raspberry/xyz/'
    name = path + 'xyz(' + str(i) + ').json'
    with open(name) as f:
        file = json.load(f)
        data.append(file)

model = data[0]

# for i in range(0, 5):
#     sign = model[str(i)]
#     plt.subplot(5, 1, i + 1)

sign = model[str(1)]
plt.plot(sign['t'], sign['x'], 'g', label='x')
plt.plot(sign['t'], sign['y'], 'r', label='y')
plt.plot(sign['t'], sign['z'], 'y', label='z')
plt.plot(sign['t'], sign['sma'], 'b', label='sma')

plt.legend(loc='upper left')
plt.show()
