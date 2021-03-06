import json
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from initPortfolio import Portfolio


# Import key from Alpha Vantage
key = "STHA8AW4L2LOMCWT"
ticker = ""

def initializeTicker(tick):
    # p1 = Portfolio({"KO": 200, "REV": 259, "GM": 237})
    p1 = Portfolio(holdings={"ABM": 200, "TSLA": 400, "KO": 76, "GE": 58, "GM": 79,
                    "AAPL": 200, "NCR" : 350, "NOK": 21, "QSR" : 240, "MMM" : 58,
                    "TAK" : 79, "SPY": 721, "DIA": 270, "FNCL": 32, "F":90})
    data = p1.perfDataCleaned
    #performance_data = 'https://www.blackrock.com/tools/hackathon/performance?datesAsStrings=true&identifiers={}'.format(ticker)
    #api = requests.get(performance_data).json()
    #data = api['resultMap']['RETURNS'][0]


    daily = data[0]['returnsMap']
    day_list = sorted(daily.items())
    return day_list

# sector = "technology"
# securities_data = 'https://www.blackrock.com/tools/hackathon/search-securities?datesAsStrings=true&query={}'.format(sector)
# apiSecurity = requests.get(securities_data).json()
# dataS = apiSecurity['resultMap']['SEARCH_RESULTS'][0]['resultList']

def check_data(data):
#     '''
#     Ensures that the API call returns data (and does not return too-many-calls notice)
#
#     Parameters:
#         data: the data to verify, should be a dictionary
#
#     Raises ValueError if API call does not return data
#     '''
    if 'Note' in data.keys():
        raise ValueError("Too many API calls, did not return data")
    return data

"""
This method uses the black rock API to give the top 5 performers in the a specific sector in the economy.
Returns: A table of top 5 tickers and their respective Market Caps
"""


def drawSectorPlots(sector):
    plt.show()
    from suggestions import companiesPerSector
    from br_api_tests import get_performanceData

    sector_dict = companiesPerSector()
    # Given sector dictionary and desired sector, create a plot of the overall growth of the sector
    # Based on the values of those securities
    if sector not in sector_dict:
        return "Sector not in dictionary, try another   "

    topNPerformers = 5

    # sorts stocks in order of increasing market cap, next line puts in order of decreasing market cap
    sortedStocks = [(ticker, mktCap) for ticker, mktCap in sorted(sector_dict[sector], key=lambda item: item[1])]
    sortedStocks.reverse()
    topNStocks = sortedStocks[:topNPerformers]

    formatted = [(ticker, f'${int(mktCap):,}') for ticker, mktCap in topNStocks]
    df = pd.DataFrame(formatted, columns=['Ticker', 'Market Cap'])
    df.set_index('Ticker', drop=True, inplace=True)
    txt = f'The Top {topNPerformers} Stocks in {sector} are:\n\n{df}'

    '''
    # calls Performance Data API on top n performers
    perfData = get_performanceData([ticker for ticker,_ in topNStocks], retNumHoldings=False)['resultMap']['RETURNS']


    plot_len = 365 # Show past year
    dates = []
    total_levels = np.zeros(plot_len)
    # Iterate through securities:
    for i in range(topNPerformers):
        daily = perfData[i]['returnsMap']
        day_list = sorted(daily.items())
        shortened_list = day_list[-plot_len:] # Grab only last year of perfData
        first_level = shortened_list[0][1]['level']
        for n in range(plot_len):
            total_levels[n] += shortened_list[n][1]['level']*sector_dict[sector][i][1]/first_level
    for i in range(plot_len):
        dates.append(dt.datetime.strptime(shortened_list[i][0],'%Y%m%d').date())
    total_levels /= total_levels[0]
    plt.plot(dates, total_levels)
    plt.title(sector.upper() + " PERFORMANCE")
    plt.savefig('sectorPerformers.png')
    plt.xlabel("DATE")
    plt.ylabel("ADJUSTED RETURNS")
    plt.show()
    '''
    return txt


"""
This method uses the alpha vantage API to get search for a specific ticker.
Returns: A graph plotted for stock price vs Date since the inception of the IPO
"""


def drawTickerPlots(ticker):

    price_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={key}&outputsize=full'
    price_data = check_data(requests.get(price_url).json())
    price_data = price_data['Time Series (Daily)']
    dateList = []
    closeList = []
    for date in price_data:
        dateList.append(dt.datetime.strptime(date, '%Y-%m-%d').date())
        closeList.append(float(price_data[date]['5. adjusted close']))
    plt.plot(dateList, closeList)

    plt.title(ticker.upper() + " DATA")
    plt.xlabel("DATE")
    plt.ylabel("SHARE PRICE ($)")

    plt.savefig("Images/searchedTicker.png")  # saves plot in particular location
    plt.show()

# Main for testing
if __name__ == '__main__':
    import random
    p1 = Portfolio(holdings={"ABM": 200, "TSLA": 400, "KO": 76, "GE": 58, "GM": 79,
                    "AAPL": 200, "NCR" : 350, "NOK": 21, "QSR" : 240, "MMM" : 58,
                    "TAK" : 79, "SPY": 721, "DIA": 270, "FNCL": 32, "F":90})
    drawTickerPlots(random.choice(list(p1.holdings.keys())))
    drawSectorPlots('Information Technology')
    # drawSectorPlots('Information Technology')
