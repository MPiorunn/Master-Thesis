import matplotlib.pyplot as plt
import json
from scipy.stats import pearsonr

velocity = [500, 900, 1400]
posuw = {
    'tabela-2-5-1-1': 0.08,
    'tabela-2-5-2-1': 0.13,
    'tabela-2-5-3-1': 0.08,
    'tabela-2-5-4-1': 0.2,
    'tabela-2-5-5-1': 0.13,
    'tabela-2-5-6-1': 0.2
}
tabs = []
name = 'tabelki.json'
with open(name) as f:
    tabs.append(json.load(f))
    tabs = tabs[0]

i = 1
charts = {}
for tab in tabs:
    for data in tabs[tab]:
        variable = tabs[tab][data]
        d, s = pearsonr(velocity, variable)
        plt.xlabel('Predkość')
        plt.ylabel(data)
        plt.plot(velocity, variable, marker='o')

        title = tab + ', F = ' + str(posuw[tab]) + ' [mm/obr], korelacja : ' + str(d)
        plt.title(title)
        plt.figure()
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


plt.show()
