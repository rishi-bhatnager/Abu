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
sectorDict = {'tech': ['AAPL','TSLA']}
sector = 'tech'


def drawSectorPlots(sectorDict, sector):
    if sector in SectorDict:
        perf_url = 'https://www.blackrock.com/tools/hackathon/performance?identifiers='
        for company in SectorDict[sector]:
            perf_url += company + '%2C'
        perf_url = perf_url[:-3]
        print(perf_url)

drawSectorPlots(sectorDict, sector)

"""
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

    drawTickerPlots(100)
"""


# if __name__ == '__main__':
