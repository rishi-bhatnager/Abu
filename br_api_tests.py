# General tests of BlackRock API, notes on capabilities

import requests, json

portfolioAnalysis_data = 'https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExpectedReturns=true& \
    calculateExposures=true&calculatePerformance=true&calculateRisk=true&includeChartData=true&positions=AAPL~50&returnAllDates=false'
api = requests.get(portfolioAnalysis_data).json()

data = api['resultMap']['PORTFOLIOS'][0]['portfolios'][0]
daily = data['returns']['returnsMap']
lastDay = sorted(daily.items())

# daysBack = 3
# for i in range(0,daysBack):
#     print(lastDay[-daysBack:][i][1]['level'])

expReturns = data['expectedReturns']
print(expReturns)


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
