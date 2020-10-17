import json
import requests
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
"""
returning the graph for each security
"""
ticker = "AAPL"
performance_data = 'https://www.blackrock.com/tools/hackathon/performance?datesAsStrings=true&identifiers={}'.format(ticker)
api = requests.get(performance_data).json()
data = api['resultMap']['RETURNS'][0]
daily = data['returnsMap']
day_list = sorted(daily.items())

sector = "technology"
securities_data = 'https://www.blackrock.com/tools/hackathon/search-securities?datesAsStrings=true&query={}'.format(sector)
apiSecurity = requests.get(securities_data).json()
dataS = apiSecurity['resultMap']['SEARCH_RESULTS'][0]['resultList']
sector_dict = {'tech': ['AAPL','TSLA','SNAP','LYFT']}
sector = 'tech'


def drawSectorPlots(sector_dict, sector):
    #Given sector dictionary and desired sector, create a plot of the overall growth of the sector
    #Based on the values of those securities
    if sector not in sector_dict:
        raise Exception("Sector not in dictionary")
    url = 'https://www.blackrock.com/tools/hackathon/performance?datesAsStrings=true&identifiers='
    for company in sector_dict[sector]:
        url += company + '%2C'
    url = url[:-3]
    api = requests.get(url).json()
    data = api['resultMap']['RETURNS'] # List of securities

    plot_len = 365 # Show past year
    dates = []
    total_levels = np.zeros(plot_len)
    # Iterate through securities:
    for i in range(len(sector_dict[sector])):
        daily = data[i]['returnsMap']
        day_list = sorted(daily.items())
        shortened_list = day_list[-plot_len:] # Grab only last year of data
        first_level = shortened_list[0][1]['level']
        for n in range(plot_len):
            total_levels[n] += shortened_list[n][1]['level']/first_level
    for i in range(plot_len):
        dates.append(dt.datetime.strptime(shortened_list[i][0][0:10],'%Y-%m-%d').date())
    total_levels = total_levels/3
    plt.plot(dates, total_levels)
    plt.title(sector.upper() + " PERFORMANCE")
    plt.show()


def drawTickerPlots(years):
    # print(day_list[0])
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
    drawTickerPlots(100)
    ## drawSectorPlots(sector_dict, 'tech')
