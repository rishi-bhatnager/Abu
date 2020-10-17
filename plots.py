# Script for testing the BlackRock API

import requests
import numpy as np
import matplotlib.pyplot as plt

response = requests.get("https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExposures=true&calculatePerformance=true&positions=AAPL~20")

returnsMap = response.json()['resultMap']['PORTFOLIOS'][0]['portfolios'][0]['returns']['returnsMap']

plot_len = 200
levels = np.ones(plot_len-1)
lastN = sorted(returnsMap.items())[-plot_len:]
for i in range(plot_len-1):
    levels[i] = lastN[i][1]['level']
plt.plot(levels)
plt.show()
print('done')
