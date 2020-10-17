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
sector_dict = {'tech': ['AAPL','TSLA','SNAP']}
sector = 'tech'


def drawSectorPlots(sector_dict, sector):
    if sector in sector_dict:
        url = 'https://www.blackrock.com/tools/hackathon/performance?identifiers='
        for company in sector_dict[sector]:
            url += company + '%2C'
        url = url[:-3]
        api = requests.get(url).json()
        data = api['resultMap']['RETURNS']
        for security in data:
            print(security['latestPerf']['oneYear'])


def drawTickerPlots(years):
    # print(day_list[0])
    plot_len = 365*years
    if len(day_list) < plot_len:
        plot_len = len(day_list)

    levels = np.ones(plot_len - 1)
    dates = []
    lastN = day_list[-plot_len:]
    for i in range(len(lastN)-1):
        print(type(dt.datetime.strptime(lastN[i][0][0:10],'%Y-%m-%d').date()))
        dates.append(dt.datetime.strptime(lastN[i][0][0:10],'%Y-%m-%d').date())
    print(dates)
    for i in range(plot_len - 1):
        # print(lastN[i])
        # dates[i] = lastN[i][0]
        levels[i] = lastN[i][1]['level']
    plt.plot(dates, levels)
    plt.show()


if __name__ == '__main__':
    # drawTickerPlots(100)
    drawSectorPlots(sector_dict, sector)
