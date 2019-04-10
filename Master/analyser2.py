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

print(data)
