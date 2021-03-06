# Script for testing the BlackRock API

from initPortfolio import Portfolio
import json
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

key = "STHA8AW4L2LOMCWT"

"""
adict is a dictionary of the users portfolio
"""
# p1 = Portfolio({"ABM": 200, "TSLA": 400, "KO": 76})
p1 = Portfolio(holdings={"ABM": 200, "TSLA": 400, "KO": 76, "GE": 58, "GM": 79,
                    "AAPL": 200, "NCR" : 350, "NOK": 21, "QSR" : 240, "MMM" : 58,
                    "TAK" : 79, "SPY": 721, "DIA": 270, "FNCL": 32, "F":90})
bigData = p1.portAnalCleaned
#response = requests.get('https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExpectedReturns=true&\
    #calculateExposures=true&calculatePerformance=true&calculateRisk=true&includeChartData=true&positions=AAPL~150%7CTSLA~50%7CSPY~100')
    #bigData = response.json()['resultMap']['PORTFOLIOS'][0]['portfolios'][0]
    #returns = bigData['returns']


def pie(data, var):
    '''
    Creates a pie chart with the given data (a dict)
    '''
    plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')

    # must have at least one of the following commented out

    if var == 'a':
        plt.title("Breakdown by Security Type")
        plt.savefig("Images/byAssetType.png")
    elif var == 'i':
        plt.title("Breakdown by Industry")
        plt.savefig('Images/byIndustry.png')
    elif var == 'g':
        plt.title("Breakdown by Sector")
        plt.savefig('Images/bySector.png')
    elif var == 'h':
        plt.title("Breakdown by Security")
        plt.savefig("Images/bySecurity.png")
    plt.show()


def levels():
    returnsMap = bigData['returns']['returnsMap']
    plot_len = min(200, len(returnsMap.keys()))
    levels = np.ones(plot_len - 1)
    shortened_list = sorted(returnsMap.items())[-plot_len:]
    dates = []
    for i in range(plot_len - 1):
        levels[i] = shortened_list[i][1]['level']
        dates.append(dt.datetime.strptime(shortened_list[i][0][0:10], '%Y%m%d').date())
    plt.plot(dates, levels)

    plt.xlabel("Months")
    plt.ylabel("Percent Growth")
    plt.title("Portfolio Growth over Time")
    plt.savefig("Images/general.png")
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
    for stat, data in analyticsMap:
        stats[stat] = data['harmonicMean']


def trendMonths():
    trendMonths = {'down': bigData['returns']['downMonths'], 'up': bigData['returns']['upMonths'], 'nochange': bigData['returns']['downMonths']}
    trendMonthPercents = {'down': bigData['returns']['downMonthsPercent'], 'up': bigData['returns']['upMonthsPercent'], 'nochange': bigData['returns']['nochangeMonthsPercent']}



def tablePortfolio():
    '''
    Makes a table summarizing the portfolio info in a Pandas DataFrame
    '''
    from br_api_tests import get_levels
    shares = getHoldings(bigData['holdings'])
    yields = get_levels(shares.keys(), retNumHoldings=False)
    zipped = [(ticker, shareCount, round(yields[ticker], 2)) for ticker, shareCount in shares.items()]
    df = pd.DataFrame(zipped, columns=['Ticker', 'Shares', 'Yield'])
    df.set_index('Ticker', drop=True, inplace=True)
    return str(df)
    # print(df)


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
            key = security[category]

        try:
            catCounts[key] += 1
        except KeyError:
            catCounts[key] = 1

    pie(catCounts, category[0])


def portfolioSpecificData(ticker):
    price_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={key}&outputsize=full'
    price_data = requests.get(price_url).json()
    price_data = price_data['Time Series (Daily)']
    price_data = sorted(price_data.items())
    latest_close = float(price_data[-1][1]['5. adjusted close'])
    monthly_return = latest_close - float(price_data[-23][1]['5. adjusted close'])
    yearly_return = latest_close - float(price_data[-255][1]['5. adjusted close'])
    df = pd.DataFrame({"Last Close ": [latest_close],
                       "Monthly return ": [monthly_return],
                       "Yearly return ": [yearly_return],
                       })
    df.rename(index={0: ticker}, inplace=True)
    return str(df)


def sectors():
    holdingsData('gics1Sector')


def industries():
    holdingsData('issFtse1Industry')


def assetTypes():
    holdingsData('assetType')


if __name__ == '__main__':
    print(tablePortfolio())
    assetTypes()
    industries()
    sectors()
    levels()
    portfolioSpecificData("TSLA")
