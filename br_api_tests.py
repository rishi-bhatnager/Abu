# General tests of BlackRock API, notes on capabilities

import requests, json

portfolioAnalysis_data = 'https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExpectedReturns=true& \
    calculateExposures=true&calculatePerformance=true&calculateRisk=true&includeChartData=true&positions=AAPL~150%7CTSLA~50&returnAllDates=false'
api = requests.get(portfolioAnalysis_data).json()


data = api['resultMap']['PORTFOLIOS'][0]['portfolios'][0]
daily = data['returns']['returnsMap']
lastDay = sorted(daily.items())

# daysBack = 3
# for i in range(0,daysBack):
#     print(lastDay[-daysBack:][i][1]['level'])

expReturns = data['expectedReturns']
# print(expReturns)

def get_risk():
    # Calculate Risk
    holdings = data['holdings']
    shares = 0
    for security in holdings:
        shares += security['weight']

    portfolio_risk = data['riskData']['totalRisk']

    spyURL = 'https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExpectedReturns=true& \
        calculateExposures=true&calculatePerformance=true&calculateRisk=true&includeChartData=true&positions=SPY~{}&returnAllDates=false'.format(shares)
    spy_data = requests.get(spyURL).json()
    spy_risk = spy_data['resultMap']['PORTFOLIOS'][0]['portfolios'][0]['riskData']['totalRisk']

    beta = portfolio_risk / spy_risk
    return beta

def get_rank():
    numHoldings = 0
    perf_url = 'https://www.blackrock.com/tools/hackathon/performance?identifiers='
    for holding in data['holdings']:
        perf_url += holding['ticker'] + '%2C'
        numHoldings += 1
    perf_url = perf_url[:-3]
    api = requests.get(perf_url).json()

    # Keys are levels, values are ticker
    levels = {}
    securities = api['resultMap']['RETURNS']
    for security in range(len(securities)):
        level = securities[security]['latestPerf']['level']
        levels[level] = securities[security]['ticker']

    split = min(3, numHoldings)
    bottomSplit = split // 2
    topSplit = split - bottomSplit
    topPerformers = sorted(levels.items())[-topSplit:]
    bottomPerformers = sorted(levels.items())[:bottomSplit]
    # print(f'Your top performers are:\n{topPerformers[0][1]} (total yield: {topPerformers[0][0]:.3f}%)')
    # print(f'Your bottom performers are:\n{bottomPerformers[0][1]} (total yield: {bottomPerformers[0][0]:.3f}%)')

get_rank()



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
