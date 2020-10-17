# Script for testing the BlackRock API

import requests
import numpy as np
import matplotlib.pyplot as plt

response = requests.get("https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExpectedReturns=true&calculateExposures=true \
&calculatePerformance=true&calculateRisk=true&positions=AAPL~150%7CTSLA~50")

bigData = response.json()['resultMap']['PORTFOLIOS'][0]['portfolios'][0]
returnsMap = bigData['returns']['returnsMap']

show_levels = False
if show_levels:
    plot_len = 200
    levels = np.ones(plot_len-1)
    lastN = sorted(returnsMap.items())[-plot_len:]
    for i in range(plot_len-1):
        levels[i] = lastN[i][1]['level']
    plt.plot(levels)
    plt.show()
    print('done')


holdings = bigData['holdings']
portfolio = {}
for security in holdings:
    portfolio[security['ticker']] = security['weight']

plt.pie(portfolio.values(),labels=portfolio.keys(),autopct='%1.1f%%')
plt.show()
