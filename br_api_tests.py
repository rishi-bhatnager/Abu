# General tests of BlackRock API, notes on capabilities

import requests, json
import pandas as pd
from initPortfolio import Portfolio


# portfolioAnalysis_data = 'https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExpectedReturns=true& \
#     calculateExposures=true&calculatePerformance=true&calculateRisk=true&includeChartData=true&positions=AAPL~150%7CTSLA~50&returnAllDates=false'
# api = requests.get(portfolioAnalysis_data).json()


# data = api['resultMap']['PORTFOLIOS'][0]['portfolios'][0]
port = Portfolio(holdings={"ABM": 200, "TSLA": 400, "KO": 76, "GE": 58, "GM": 79,
                    "AAPL": 200, "NCR" : 350, "NOK": 21, "QSR" : 240, "MMM" : 58,
                    "TAK" : 79, "SPY": 721, "DIA": 270, "FNCL": 32, "F":90})
data = port.portAnalCleaned
daily = data['returns']['returnsMap']
lastDay = sorted(daily.items())

'''
data['resultMap']['PORTFOLIOS'][0]['portfolios'][0] has the important stuff (it's a dict, see online tester for all the keys)
Key: analyticsMap
  includes P/E and P/B ratios, as well as returnOnAssets, returnOnEquity, twelveMonthTrailingYield
Key: expectedReturns (if that option is selected)
Key: holdings
    Has extra info for funds (incluing fund-specific analytics and top holdings)
Key: returns (the bulk of the data) -- this is a dict
  Keys: downMonths, downMonthsPercent, upMonths, upMonthsPercent, nochangeMonths, nochangeMonthsPercent
  Key: latestPerf (a dict)
      Keys: sharpe ratios, risk at various time periods
  Key: returnsMap (a dict with keys of dates in format YYYYMMDD, each date maps to )
  Key: riskData
      Most important key: totalRisk
          (can query API for this value for SPY, and compare holdings' totalRisk to SPY's for a risk relative to the S&P)
'''


def get_risk(ticker,shares):
    # Calculate Risk

    portfolio_risk = data['riskData']['totalRisk']

    spyURL = 'https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExpectedReturns=true& \
        calculateExposures=true&calculatePerformance=true&calculateRisk=true&includeChartData=true&positions=SPY~{}&returnAllDates=false'.format(
        shares)
    spy_data = requests.get(spyURL).json()
    spy_risk = spy_data['resultMap']['PORTFOLIOS'][0]['portfolios'][0]['riskData']['totalRisk']

    beta = portfolio_risk / spy_risk
    return beta


def get_performanceData(holdings, retNumHoldings=True):
    '''
    Gets the Performance Data for a portfolio (i.e. the performance of each individual security in a portfolio)

    Params:
        holdings: an iterable containing tickers of the holdings of a portfolio
        retNumHoldings: if True, returns the number of holdings in the portfolio

    Returns:
        final: a dict representing the json returned by the appropriate Performance Data API call
        numHoldings: the number of securities the portfolio contains (only returned if assoc. param set to True)
    '''
    numHoldings = 0
    perf_url = 'https://www.blackrock.com/tools/hackathon/performance?identifiers='
    for holding in holdings:
        perf_url += holding + '%2C'
        numHoldings += 1
    perf_url = perf_url[:-3]
    final = requests.get(perf_url).json()

    if retNumHoldings:
        return final, numHoldings
    else:
        return final


def get_levels(holdings, retNumHoldings=True):
    '''
    Gets the levels for each security in the portfolio

    Params:
        holdings: an iterable containing the holdings to look at (list of securities)
        retNumHoldings: if True, returns the number of holdings in the portfolio

    Returns:
        levels: a dictionary mapping tickers to their levels (yield)
        numHoldings: the number of securities the portfolio contains (only returned if assoc. param set to True)
    '''
    perfData, numHoldings = get_performanceData(holdings)

    levels = {}
    securities = perfData['resultMap']['RETURNS']
    for security in securities:
        if 'ticker' in security.keys():
            levels[security['ticker']] = security['latestPerf']['level']
        else:
            levels[security['uniqueId']] = security['latestPerf']['level']

    if retNumHoldings:
        return levels, numHoldings
    else:
        return levels


def getHoldingsList(holdingsData):
    '''
    Returns the list of tickers of holdings given the holdings as returned by Portfolio Analysis API
    '''
    holdings = []
    for holding in holdingsData:
        holdings.append(holding['ticker'])
    return holdings


def get_rank(called_from_sector_rank=False):
    levels, numHoldings = get_levels(getHoldingsList(data['holdings']))

    # sorts levels (next line puts in order of decreasing value) into list of size-2 tuples containing the (tcker,level)
    levels = [(k, v) for k, v in sorted(levels.items(), key=lambda item: item[1])]
    # levels.reverse()

    split = min(3, numHoldings)
    bottomSplit = split // 2
    topSplit = split - bottomSplit
    topPerformers = levels[-topSplit:]
    bottomPerformers = levels[:bottomSplit]

    # topTable = pd.DataFrame(columns=["Tick", "Yield"])
    txt = 'Your top performers:\n'
    for top in topPerformers:
        # temp = pd.DataFrame([[top[0], top[1]]], columns=["Tick", "Yield"])
        # topTable = topTable.append(temp, ignore_index=True)
        txt = txt + (f'{top[0]}, total yield: {top[1]:.3f}\n')
    txt = txt + ('\nYour bottom performers:\n')

    # bottable = pd.DataFrame(columns=["Tick", "Yield"])
    for bottom in bottomPerformers:
        # temp = pd.DataFrame([[bottom[0], bottom[1]]], columns=["Tick", "Yield"])
        # bottable = bottable.append(temp, ignore_index=True)
        txt = txt + f'{bottom[0]}, total yield: {bottom[1]:.3f}\n'
    '''
    resultA = topTable.to_json(orient="split")
    parsed = json.loads(resultA)
    print (json.dumps(parsed, indent=4))
    print(topTable)
    return parsed
    '''
    return txt


def get_sector_rank():
    holdings = data['holdings']

    # will map sectors to the number of shares they contain (in total)
    sectorShares = {}

    # maps tickers to a tuple containing its level, number of shares, and sector (in that order)
    portfolio = {}

    levels = get_levels(getHoldingsList(holdings), retNumHoldings=False)
    for security in holdings:
        if security['assetType'] == 'Fund':
            sector = 'Funds'
        else:
            sector = security['gics1Sector']

        shares = security['weight']
        ticker = security['ticker']
        portfolio[ticker] = (levels[ticker], shares, sector)

        try:
            sectorShares[sector] += shares
        except KeyError:
            sectorShares[sector] = shares

    # maps sectors to their weighted level
    sectorLevels = {}
    for ticker, (level, shares, sector) in portfolio.items():
        weightedLevel = (shares / sectorShares[sector]) * level
        try:
            sectorLevels[sector] += weightedLevel
        except KeyError:
            sectorLevels[sector] = weightedLevel

    # sorts sectorLevels (next line puts in order of decreasing value) into list of size-2 tuples containing the (sector,weightedLevel)
    sectorLevels = [(k, v) for k, v in sorted(sectorLevels.items(), key=lambda item: item[1])]
    sectorLevels.reverse()
    txt = 'Your top performing sectors:\n'

    for sector, level in sectorLevels:
        txt = txt + (f'{sector}, weighted yield: {level:.3f}\n')
    return txt

def get_both():
    return [get_rank(), get_sector_rank()]

if __name__ == '__main__':
    print(get_both())
