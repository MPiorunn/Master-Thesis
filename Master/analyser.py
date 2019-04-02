import matplotlib.pyplot as plt
import numpy as np
from fastdtw import fastdtw
from scipy import signal


def read():
    for i in range(1, files):
        name = "stasiu/data(" + str(i) + ").txt"
        file = open(name, "r")
        t = np.float_(file.readline().replace("t[", "").replace("]", "").replace("\n", "").split(", "))
        mag = np.float_(file.readline().replace("MAG [", "").replace("]", "").replace("\n", "").split(", "))
        sma = np.float_(file.readline().replace("SMA [", "").replace("]", "").split(", "))
        times.append(t)
        peaks.append(signal.find_peaks(sma))
        # plt.subplot(files / 2, 2, i)
        # plt.plot(t, sma)
        # plt.plot(t[peaks[i - 1][0]], sma[peaks[i - 1][0]])
        # if i != (files - 1):
        #     plt.xticks([], [])
    # plt.show()


def forgery():
    for i in range(1, forgedFiles):
        name = "ja/data" + str(i) + ".txt"
        file = open(name, "r")

        t = np.float_(file.readline().replace("t[", "").replace("]", "").replace("\n", "").split(", "))
        mag = np.float_(file.readline().replace("MAG [", "").replace("]", "").replace("\n", "").split(", "))
        sma = np.float_(file.readline().replace("SMA [", "").replace("]", "").split(", "))
        forgedTimes.append(t)
        forgedPeaks.append(signal.find_peaks(sma))
        # plt.subplot(files / 2, 2, i)
        # plt.plot(t, sma)
        # plt.plot(t[forgedPeaks[i - 1][0]], sma[forgedPeaks[i - 1][0]])
        # if i != (files - 1):
        #     plt.xticks([], [])
    # plt.show()






maximums = []
files = 11
forgedFiles = 6
times = []
forgedTimes = []
peaks = []
forgedPeaks = []
writeTimes = []
writeFTimes = []
# read()
distances = []
forgedDistances = []
avgForgedDistances = []
read()
forgery()

for i in range(0, len(peaks)):
    tLen = len(times[i]) - 1
    writeTimes.append(times[i][tLen])
    for j in range(0, len(peaks)):
        if i != j:
            distance, path = fastdtw(peaks[i][0], peaks[j][0])
            distances.append(distance)

for i in range(0, len(forgedPeaks)):
    tLen = len(forgedTimes[i]) - 1
    writeFTimes.append(forgedTimes[i][tLen])
    for j in range(0, len(peaks)):
        if i != j:
            distance, path = fastdtw(forgedPeaks[i][0], peaks[j][0])
            forgedDistances.append(distance)
    avgForgedDistances.append(np.median(forgedDistances))

print("Average write time : " + str(np.average(writeTimes)))
print("Average write forgery time : " + str(np.average(writeFTimes)))

print("Median write time : " + str(np.median(writeTimes)))
print("Median write forgery time : " + str(np.median(writeFTimes)))

print("Average dtw : " + str(np.average(distances)))
print("Average dtw forged : " + str(np.average(forgedDistances)))

print("Median DTW forged : " + str(np.median(forgedDistances)))
print("Median DTW : " + str(np.median(distances)))
print(avgForgedDistances)
writeTimes.sort()
print(writeTimes)