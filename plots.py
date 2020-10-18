# Script for testing the BlackRock API

import pandas as pd
import json
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


response = requests.get('https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExpectedReturns=true&\
    calculateExposures=true&calculatePerformance=true&calculateRisk=true&includeChartData=true&positions=AAPL~150%7CTSLA~50%7CSPY~100')

bigData = response.json()['resultMap']['PORTFOLIOS'][0]['portfolios'][0]
returns = bigData['returns']


def pie(data, var):
    '''
    Creates a pie chart with the given data (a dict)
    '''
    plt.pie(data.values(),labels=data.keys(),autopct='%1.1f%%')

    # must have at least one of the following commented out

    if var == 'a':
        plt.savefig("byAssetType.png")
    elif var == 'i':
        plt.savefig('byIndustry.png')
    elif var == 'g':
        plt.savefig('bySector.png')
    elif var == 'h':
        plt.savefig("bySecurity.png")
    plt.show()

def levels():
    returnsMap = returns['returnsMap']
    plot_len = min(200, len(returnsMap.keys()))
    levels = np.ones(plot_len - 1)
    lastN = sorted(returnsMap.items())[-plot_len:]
    for i in range(plot_len - 1):
        levels[i] = lastN[i][1]['level']
    plt.plot(levels)
    plt.savefig("general.png")
    plt.show()



def getHoldings(portfolio):
    '''
    Returns a dict that maps tickers of holdings in given portfolio to the number of shares in the portfolio
    '''
    shares = {}
    for security in portfolio:
        shares[security['ticker']] = security['weight']

    return shares


def holdings():
    portfolio = getHoldings(bigData['holdings'])
    pie(portfolio, 'h')


def analyticsMap():
    analyticsMap = bigData['analyticsMap']
    stats = {}
    for stat,data in analyticsMap:
        stats[stat] = data['harmonicMean']

def trendMonths():
    trendMonths = {'down': returns['downMonths'], 'up': returns['upMonths'], 'nochange': returns['downMonths']}
    trendMonthPercents = {'down': returns['downMonthsPercent'], 'up': returns['upMonthsPercent'], 'nochange': returns['nochangeMonthsPercent']}


def tablePortfolio():
    '''
    Makes a table summarizing the portfolio info in a Pandas DataFrame
    '''
    from br_api_tests import get_levels
    shares = getHoldings(bigData['holdings'])
    yields = get_levels(shares.keys(), retNumHoldings=False)
    zipped = [(ticker, shareCount, round(yields[ticker],2)) for ticker,shareCount in shares.items()]


    df = pd.DataFrame(zipped, columns=['Ticker', 'Shares', 'Yield'])
    # i = 0
    # for ticker in shares:
    #     df[i] = [ticker, shares[ticker], yields[ticker]]
    #     i += 1
    df.set_index('Ticker', drop=True, inplace=True)

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

    pie(catCounts, category[0])


def sectors():
    holdingsData('gics1Sector')


def industries():
    holdingsData('issFtse1Industry')

def assetTypes():
    holdingsData('assetType')


if __name__ == '__main__':
    tablePortfolio()
    assetTypes()
    industries()
    sectors()
    levels()
