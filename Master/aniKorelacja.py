import matplotlib.pyplot as plt
import json
from scipy.stats import pearsonr
import xlsxwriter
import numpy as np

velocity = [500, 900, 1400]
posuw = {
    'tabela-2-5-1-1': 0.08,
    'tabela-2-5-2-1': 0.13,
    'tabela-2-5-3-1': 0.08,
    'tabela-2-5-4-1': 0.2,
    'tabela-2-5-5-1': 0.13,
    'tabela-2-5-6-1': 0.2
}

predkosci = {
    'tabela-2-9': 1400,
    'tabela-2-1-1': 1400,
    'tabela-2-3-1': 900,
    'tabela-2-2-1': 900,
    'tabela-2-4-1': 560,
    'tabela-2-5-7': 560,
}
tabs = []
name = 'tabelki2.json'
with open(name) as f:
    tabs.append(json.load(f))
    tabs = tabs[0]
workbook = xlsxwriter.Workbook('Korelacje.xlsx')
worksheet = workbook.add_worksheet()
i = 1

charts = {}
for tab in tabs:
    for data in tabs[tab]:
        variable = tabs[tab][data]
        d, s = pearsonr(velocity, variable)
        # plt.xlabel('Predkość')
        # plt.ylabel(data)
        # plt.plot(velocity, variable, marker='o')

        # title = tab + ', F = ' + str(posuw[tab]) + ' [mm/obr], zmienna : ' + data + ' korelacja : ' + str(d)
        # print()
        charts[i] = {
            "t": tab,
            "p": str(predkosci[tab]),
            "d": data,
            "k": str(d)
        }
        print(charts[i])
        # plt.title(title)
        # plt.figure()
        i += 1
'''
wykres wymiaru fraktalnego od posuwu
wykresy wszystkiego od posuwu
korelacje 
'''

# for i in range(1, len(charts)):
#     j = i % 7
#     if j == 0:
#         j = 7
#         plt.figure()
#     print(j)
#     plt.subplot(7, 1, j)
#     plt.xlabel('Predkość')
#     plt.ylabel(charts[i]['data'])
#     plt.plot(velocity, charts[i]['variable'])


# plt.show()

# zaczynamy w pierwszej kolumnie pierwszym rzędzie

row = 0
col = 1
for i in range(1, len(charts) + 1):
    # wypisujemy tytuł tabelki
    if col != 1 and col % 2 == 0:
        row = row + 6
    # jeżeli wypisaliśmy 2 , przechodzimy 2 niżej, czyli row += 6
    worksheet.write(row, 0, charts[i]["t"])
    # idziemy linijkę niżej i wypisujemy posuw
    posuf = 'Prędkość : ' + charts[i]["p"]
    worksheet.write(row + 1, 0, posuf)
    # wypisujemy zmienną
    worksheet.write(row + 2, 0, charts[i]["d"])
    # wypisujemy korelacje
    worksheet.write(row + 3, 0, charts[i]["k"])
    # idziemy jedną w prawo
    col = col + 1

workbook.close()

list = [
    0.34094235519457894,
    0.5823811350562264,
    0.4844275785848916,
    0.46809216272264736,
    0.4620438215402159,
    0.4824182238653514,
    0.6165808956951864,
    0.4792519651056505
]

print('xD')
av = np.average(list)
print(av)
print(av * 0.95)
print(av * 1.05)
print()
print(av * 0.98)
print(av * 1.02)
print()
print(av * 0.90)
print(av * 1.1)
