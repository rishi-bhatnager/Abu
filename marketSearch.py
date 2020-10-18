import json
import requests
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

key = "STHA8AW4L2LOMCWT"

def plotMarket(tick):
    from securitySearch import check_data
    ticker = tick
    # Url to get data, other options include:
    #   * function=TIME_SERIES_DAILY_ADJUSTED for adjusted close prices (i.e. not raw data)
    #       ** there are different functions (including intraday data), see documentation for more
    #   * outputsize=full for full time series data (20+ years worth)
    #       ** default is 100 most recent
    #   * datatype=csv outputs csv
    #       ** default is json
    price_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={key}'
    price_data = check_data(requests.get(price_url).json())
    # Data is a dict of many dict's (can go to url to see what the json looks like)
    # Outer dict has 2 keys: 'Meta Data' and 'Time Series (Daily)' (second key will be different for different functions used)
    # Time Series key is a dict with keys being dates
    # Each date is a dict with keys ['1. open', '2. high', '3. low', '4. close', '5. volume']
    price_data = price_data['Time Series (Daily)']
    dateList = []
    closeList = []
    for date in price_data:
        dateList.append(dt.datetime.strptime(date,'%Y-%m-%d').date())
        closeList.append(float(price_data[date]['4. close']))
    plt.plot(dateList, closeList)
    plt.ylabel("Percent Growth")
    plt.xlabel("Months")
    if tick[0] == 'S':
        plt.title('S&P 500')
        plt.savefig('S&P.png')
    else:
        plt.title("Dow Jones Industrial Average")
        plt.savefig('Dow.png')

    plt.show()

if __name__ == '__main__':
    plotMarket("SPY")
    plotMarket("DIA")
