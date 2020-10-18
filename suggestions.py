import json
import requests
import random

# sp500financials will be a list of 505 dictionaries
# NOTE: THIS DATA IS 3 MONTHS OLD (source: https://datahub.io/core/s-and-p-500-companies-financials#python)
url = 'https://pkgstore.datahub.io/core/s-and-p-500-companies-financials/constituents-financials_json/data/ddf1c04b0ad45e44f976c1f32774ed9a/constituents-financials_json.json'
sp500financials = requests.get(url).json()


# a dict that maps to a dict that maps the ticker to each corresponding data point in the json individually
#   e.g. data['Names'] is a dict that maps each ticker to its full name, like data['Names']['AAPL'] = 'Apple, Inc.'
# some columns excluded if they would change too much in the 3 months since the data was made
data = {'Names': {}, 'Sectors': {}, 'P/E': {}, 'EPS': {}, 'MktCap': {}, 'EBITDA': {}, 'P/S': {}, 'P/B': {}}

for stock in sp500financials:
    data['Names'][stock['Symbol']] = stock['Name']
    data['Sectors'][stock['Symbol']] = stock['Sector']
    data['P/E'][stock['Symbol']] = stock['Price/Earnings']
    data['EPS'][stock['Symbol']] = stock['Earnings/Share']
    data['MktCap'][stock['Symbol']] = stock['Market Cap']
    data['EBITDA'][stock['Symbol']] = stock['EBITDA']
    data['P/S'][stock['Symbol']] = stock['Price/Sales']
    data['P/B'][stock['Symbol']] = stock['Price/Book']


def companiesPerSector():
    '''
    Returns a dictionary that maps sector names to all companies in the S&P 500 in that sector
    The value will be a tuple of format: (ticker, market_cap)
    '''
    sectors = {}

    for ticker,sector in data['Sectors'].items():
        try:
            sectors[sector].append((ticker, data['MktCap'][ticker]))
        except KeyError:
            sectors[sector] = [(ticker, data['MktCap'][ticker]), ]

    return sectors


def generateSuggestions(risk='medium', sectors=['any',]):
    '''
    Gives 3 suggestions based on the given parameters

    Params:
        risk: a string representing the user's preferred risk (should be either 'low', 'medium', or 'high')
        sector: list of preferred sectors, if any ('any' allows for any sector)

    Returns:
        suggestions
    '''
    if risk not in ['low', 'medium', 'high']:
        raise ValueError(f'Risk must be \'low\', \'medium\', or \'high\'. Was {risk}')

    allSectors = list(companiesPerSector().keys())
    if 'any' in sectors:
        sectors = allSectors
    else:
        for sector in sectors:
            if sector not in allSectors:
                raise ValueError(f'Given sector does not exist. Given \'{sector}\'')



    if risk == 'low':
        etfs = {'General': ['SPY', 'DIA', 'QQQ'], }


    def sortData(metric):
        '''
        Returns a list of data sorted by the given metric

        Pararms:
            metric: the metric to sort by (ex: EPS). SHOULD BE SAME AS CORRESPONDING KEY IN DATA DICT

        Returns:
            list sorted in order of increasing metric, will be length-2 tuples of format (ticker,metric),
                will only include stocks in given sector
        '''
        return [(ticker,met) for ticker,met in sorted([(ticker,met) for ticker,met in data[metric].items()\
            if met is not None and data['Sectors'][ticker] in sectors],key=lambda item: item[1])]

    sortedPE = sortData('P/E')
    sortedEPS = sortData('EPS')
    sortedMktCap = sortData('MktCap')
    sortedEBITDA = sortData('EBITDA')
    sortedPS = sortData('P/S')
    sortedPB = sortData('P/B')

    # basically I'm classifying a "good" stock as one that is in the top quartile of the at least n of the above metrics,
    #   where n = the performanceMetric specified below
    # NOTE: market cap is not is not used as a metric to measure a "good" stock, but rather a medium vs high risk stock
    #   medium risk stocks are in the top half of the market caps, high risk stocks are in the bottom half
    # NOTE: EBITDA is not used for high risk, but medium risk suggestions will be in top half of EBITDA
    minList,minLength = None,float('inf')
    for dataList in [sortedPE, sortedEPS, sortedMktCap, sortedEBITDA, sortedPS, sortedPB]:
        if len(dataList) < minLength:
            minLength = len(dataList)
            minList = dataList

    bankSize = min(minLength, 150)
    prop = 1/2  # sets proportion to measure top stocks (e.g. if 1/3, will look for stocks in top third of each metric)
    top = round(bankSize*prop)
    performanceMetric = random.choice([2,3])

    print(sortedPE[-top:])

    # tickers for stocks in the top proportion of each metric
    topPE = []

    for stock,_ in minList:
        # will count in how many metrics this stock is in the top third
        count = 0



generateSuggestions()

