# Script for testing the BlackRock API

import json
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


response = requests.get('https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExpectedReturns=true&\
    calculateExposures=true&calculatePerformance=true&calculateRisk=true&includeChartData=true&positions=AAPL~150%7CTSLA~50%7CSPY~100')

bigData = response.json()['resultMap']['PORTFOLIOS'][0]['portfolios'][0]
returns = bigData['returns']


def pie(data):
    '''
    Creates a pie chart with the given data (a dict)
    '''
    plt.pie(data.values(),labels=data.keys(),autopct='%1.1f%%')

    # must have at least one of the following commented out
    plt.show()
    # plt.savefig('foo.png')


def levels():
    returnsMap = returns['returnsMap']
    plot_len = 200
    levels = np.ones(plot_len-1)
    lastN = sorted(returnsMap.items())[-plot_len:]
    for i in range(plot_len-1):
        levels[i] = lastN[i][1]['level']
    plt.plot(levels)
    plt.show()


def getHoldings():
    '''
    Returns a dict that maps tickers of holdings in current portfolio to the number of shares in the portfolio
    '''
    portfolio = {}
    for security in bigData['holdings']:
        portfolio[security['ticker']] = security['weight']

    return portfolio


def holdings():
    portfolio = getHoldings()
    pie(portfolio)


def analyticsMap():
    analyticsMap = bigData['analyticsMap']
    stats = {}
    for stat,data in analyticsMap:
        stats[stat] = data['harmonicMean']

def trendMonths():
    trendMonths = {'down': returns['downMonths'], 'up': returns['upMonths'], 'nochange': returns['downMonths']}
    trendMonthPercents = {'down': returns['downMonthsPercent'], 'up': returns['upMonthsPercent'], 'nochange': returns['nochangeMonthsPercent']}


def tablePortfolio():
    from br_api_tests import get_levels
    portfolioDict = getHoldings()
    yields = get_levels(portfolioDict.keys(), retNumHoldings=False)
    print(portfolioDict)
    print(yields)
    print(yields.values())


    portfolio = {'Ticker': portfolioDict.keys(),
            'Number of Shares': portfolioDict.values(),
            'Yield': yields.values(),
            }

    df = pd.DataFrame(portfolio, columns=['Ticker', 'Number of Shares', 'Yield'])
    print(df)


def holdingsData(category):
    '''
    Creates a pie chart based on the distribution of holdings over the given category (a string)
    '''
    holdings = bigData['holdings']
    catCounts = {}

    # true if category is something that funds will not have (e.g. funds don't have a sector)
    fundFlag = category.endswith('Sector') or category.endswith('Industry')
    for security in holdings:
        if fundFlag and security['assetType'] == 'Fund':
            key = 'Funds'
        else:
            key =  security[category]


        try:
            catCounts[key] += 1
        except KeyError:
            catCounts[key] = 1

    pie(catCounts)


def sectors():
    holdingsData('gics1Sector')


def industries():
    holdingsData('issFtse1Industry')

def assetTypes():
    holdingsData('assetType')


if __name__ == '__main__':
    tablePortfolio()
    """
    assetTypes()
    """

