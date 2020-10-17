# General tests of BlackRock API, notes on capabilities

import requests, json

portfolioAnalysis_data = 'https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExpectedReturns=true& \
    calculateExposures=true&calculatePerformance=true&calculateRisk=true&includeChartData=true&positions=TSLA~100&returnAllDates=false'
api = requests.get(portfolioAnalysis_data).json()

data = api['resultMap']['PORTFOLIOS'][0]['portfolios'][0]
daily = data['returns']['returnsMap']
lastDay = sorted(daily.items())

# daysBack = 3
# for i in range(0,daysBack):
#     print(lastDay[-daysBack:][i][1]['level'])

expReturns = data['expectedReturns']
# print(expReturns)

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
print(beta)


'''
data['resultMap']['PORTFOLIOS'][0]['portfolios'][0] has the important stuff (it's a dict, see online tester for all the keys)
Key: analyticsMap
  includes P/E and P/B ratios, as well as returnOnAssets, returnOnEquity, twelveMonhTrailingYield
Key: expectedReturns (if that option is selected)
Key: holdings
Key: returns (the bulk of the data) -- this is a dict
  Keys: downMonths, downMonthsPercent, upMonths, upMonthsPercent, nochangeMonths, nochangeMonthsPercent
  Key: latestPerf (a dict)
      Keys: sharpe ratios, risk at various time periods
  Key: returnsMap (a dict with keys of dates in format YYYYMMDD, each date maps to )
  Key: riskData
      Most important key: totalRisk
          (can query API for this value for SPY, and compare holdings' totalRisk to SPY's for a risk relative to the S&P)
'''
