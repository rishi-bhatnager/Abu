import json
import requests
import numpy as np
import matplotlib.pyplot as plt
"""
returning the graph for each security
"""
ticker = "AAPL"
portfolio_analysis_data = 'https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExpectedReturns=true& \
    calculateExposures=true&calculatePerformance=true&calculateRisk=true&includeChartData=true&positions={}~150%7CTSLA~50&returnAllDates=false'.format(ticker)
api = requests.get(portfolio_analysis_data).json()

data = api['resultMap']['PORTFOLIOS'][0]['portfolios'][0]
daily = data['returns']['returnsMap']
lastDay = sorted(daily.items())

def drawPlots():
    plot_len = 200
    levels = np.ones(plot_len -1)
    lastN = lastDay[-plot_len:]
    for i in range(plot_len - 1):
        levels[i] = lastN[i][1]['level']
    plt.plot(levels)
    plt.show()





