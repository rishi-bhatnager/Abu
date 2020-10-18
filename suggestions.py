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
        a list of 3 tickers of random possible securities (of those that are deemed good)
    '''
    risk = risk.lower()
    if risk not in ['low', 'medium', 'high']:
        raise ValueError(f'Risk must be \'low\', \'medium\', or \'high\'. Was {risk}')

    allSectors = list(companiesPerSector().keys())
    if 'any' in sectors:
        sectors = allSectors
    else:
        for sector in sectors:
            if sector not in allSectors:
                raise ValueError(f'Given sector does not exist. Given \'{sector}\'')


    def sortData(metric, cleanNegatives=False):
        '''
        Returns a list of data sorted by the given metric

        Pararms:
            metric: the metric to sort by (ex: EPS). SHOULD BE SAME AS CORRESPONDING KEY IN DATA DICT
            cleanNegatives: if True, will set negative metric values to inf

        Returns:
            list sorted in order of increasing metric, will be length-2 tuples of format (ticker,metric),
                will only include stocks in given sector
        '''
        dataList = list(data[metric].items())
        if cleanNegatives:
            dataList = [(ticker,(met if met >= 0 else float('inf'))) for ticker,met in sortData(metric)]

        return [(ticker,met) for ticker,met in sorted([(ticker,met) for ticker,met in dataList\
            if met is not None and data['Sectors'][ticker] in sectors],key=lambda item: item[1])]

    sortedPE = sortData('P/E', cleanNegatives=True)
    sortedEPS = sortData('EPS')
    sortedMktCap = sortData('MktCap')
    # sortedEBITDA = sortData('EBITDA')
    sortedPS = sortData('P/S', cleanNegatives=True)
    # sortedPB = sortData('P/B')

    # P/B or EBITDA not used for now
    # P/E and MktCap used to measure risk
    # EPS and P/S used to measure how good a stock is (at a basic level)
    minList,minLength = None,float('inf')
    for dataList in [sortedPE, sortedEPS, sortedMktCap, sortedPS, ]:
        if len(dataList) < minLength:
            minLength = len(dataList)
            minList = dataList

    bankSize = min(minLength, 150)
    prop = 1/2  # sets proportion to measure top stocks (e.g. if 1/3, will look for stocks in top third of each metric)
    top = round(bankSize*prop)
    topCriteria = random.choice([1,2]) # determines in how many metrics a stock must be in the top half of to be deemed "good"


    # tickers for stocks in the top proportion of each metric
    topHalf = len(sortedPE)//2
    riskyPE,safePE = sortedPE[-topHalf:],sortedPE[:(len(sortedPE)-topHalf)]

    topEPS = sortedEPS[-top:]
    topPS = sortedPS[:top]

    topHalf = len(sortedMktCap)//2
    topMktCap,bottomMktCap = sortedMktCap[-topHalf:], sortedMktCap[:(len(sortedMktCap)-topHalf)]


    riskiness = {'low': [], 'medium': [], 'high': []}
    goodStocks = set()  # stocks are defined as good if they are in the top half of EPS and PS
    for stock,_ in minList:
        if stock in [ticker for ticker,_ in safePE] and stock in [ticker for ticker,_ in topMktCap]:
            riskiness['low'].append(stock)
        elif stock in [ticker for ticker,_ in riskyPE] and stock in [ticker for ticker,_ in bottomMktCap]:
            riskiness['high'].append(stock)
        else:
            riskiness['medium'].append(stock)

        # if int(stock in [ticker for ticker,_ in topEPS]) + int(stock in [ticker for ticker,_ in topPS]) >= topCriteria:
        if stock in [ticker for ticker,_ in topEPS] or stock in [ticker for ticker,_ in topPS]:
            goodStocks.add(stock)


    possibleSecurities = [ticker for ticker in riskiness[risk] if ticker in goodStocks]
    if risk == 'low':
        etfs = {
            'General': ['SPY', 'DIA', 'QQQ'],
            'Industrials': ['FIDU', 'VIS', 'IYJ', 'RGI'],
            'Health Care': ['FHLC', 'RYH', 'XHE', 'VHT'],
            'Information Technology': ['XSW', 'FTEC', 'RYT', 'VGT'],
            'Consumer Discretionary': ['XLY', 'VCR', 'FXD', 'FDIS'],
            'Utilities': ['FUTY', 'VPU', 'RYU', 'XLU'],
            'Financials': ['FNCL', 'RYF', 'VFH', 'KIE'],
            'Materials': ['GDX', 'GDXJ', 'XLB', 'VAW'],
            'Real Estate': ['USRT', 'BBRE', 'FREL', 'XLRE'],
            'Consumer Staples': ['XLP', 'VDC', 'FSTA', 'KXI'],
            'Energy': ['XLE', 'AMLP', 'VDE', 'XOP'],
            'Telecommunication Services': ['VOX', 'NXTG', 'FCOM', 'IYZ']}

        etfsInSector = etfs['General']
        for sector in sectors:
            etfsInSector += etfs[sector]

        possibleSecurities += etfsInSector

    return random.sample(possibleSecurities, 3)


