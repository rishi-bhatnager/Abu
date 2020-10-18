import json
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
"""
returning the graph for each security
"""
ticker = ""
def initializeTicker(tick):
    ticker = tick
    performance_data = 'https://www.blackrock.com/tools/hackathon/performance?datesAsStrings=true&identifiers={}'.format(ticker)
    api = requests.get(performance_data).json()
    data = api['resultMap']['RETURNS'][0]
    daily = data['returnsMap']
    day_list = sorted(daily.items())
    return day_list

# sector = "technology"
# securities_data = 'https://www.blackrock.com/tools/hackathon/search-securities?datesAsStrings=true&query={}'.format(sector)
# apiSecurity = requests.get(securities_data).json()
# dataS = apiSecurity['resultMap']['SEARCH_RESULTS'][0]['resultList']

# sector = 'Industrials'

def drawSectorPlots(sector):
    from suggestions import companiesPerSector
    from br_api_tests import get_performanceData

    sector_dict = companiesPerSector()
    #Given sector dictionary and desired sector, create a plot of the overall growth of the sector
    #Based on the values of those securities
    if sector not in sector_dict:
        raise Exception("Sector not in dictionary")


    topNPerformers = 5

    # sorts stocks in order of increasing market cap, next line puts in order of decreasing market cap
    sortedStocks = [(ticker, mktCap) for ticker, mktCap in sorted(sector_dict[sector], key=lambda item: item[1])]
    sortedStocks.reverse()
    topNStocks = sortedStocks[:topNPerformers]

    formatted = [(ticker, f'${int(mktCap):,}') for ticker,mktCap in topNStocks]
    df = pd.DataFrame(formatted, columns=['Ticker', 'Market Cap'])
    df.set_index('Ticker', drop=True, inplace=True)
    print(f'The Top {topNPerformers} Stocks in {sector} are:\n{df}')


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
        dates.append(dt.datetime.strptime(shortened_list[i][0][0:10],'%Y%m%d').date())
    total_levels /= total_levels[0]
    plt.plot(dates, total_levels)
    plt.title(sector.upper() + " PERFORMANCE")
    plt.show()


def drawTickerPlots(years, ticker):
    # print(day_list[0])
    day_list = initializeTicker(ticker)
    plot_len = 365*years
    if len(day_list) < plot_len:
        plot_len = len(day_list)

    levels = np.ones(plot_len - 1)
    dates = []
    shortened_list = day_list[-plot_len:]
    for i in range(len(shortened_list)-1):
        dates.append(dt.datetime.strptime(shortened_list[i][0][0:10],'%Y-%m-%d').date())
    for i in range(plot_len - 1):
        levels[i] = shortened_list[i][1]['level']
    plt.plot(dates, levels)
    plt.title(ticker.upper() + " PERFORMANCE")
    plt.show()


if __name__ == '__main__':
    # drawTickerPlots(100)
    drawSectorPlots('Information Technology')
