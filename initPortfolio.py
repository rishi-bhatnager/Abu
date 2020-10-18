# pre-loads the data set and allows for custom url creation

import json, requests

class Portfolio:
    def __init__(self, holdings={'AAPL': 150,'TSLA': 50,'SPY': 100}):
        portfolio_anlaysis = 'https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExpectedReturns=true& \
            calculateExposures=true&calculatePerformance=true&calculateRisk=true&includeChartData=true&positions='
        performance_data ='https://www.blackrock.com/tools/hackathon/performance?identifiers='

        for ticker,shares in holdings.items():
            portfolio_anlaysis += f'{ticker}~{str(shares)}%7C'
            performance_data += ticker + '%2C'

        portfolio_anlaysis = portfolio_anlaysis[:-3]
        performance_data = performance_data[:-3]

        self.portAnal = requests.get(portfolio_anlaysis).json()
        self.perfData = requests.get(performance_data).json()

        self.portAnalCleaned = self.portAnal['resultMap']['PORTFOLIOS'][0]['portfolios'][0]
        self.perfDataCleaned = self.perfData['resultMap']['RETURNS']
