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


    def saveData(self, dicts=['portAnalCleaned', 'perfDataCleaned'], folder='./'):
        '''
        Saves the given data as a json file into the specified folder

        Params:
            dicts: string representataions of the names of the dictionaries to save (defaults to the cleaned data from both APIs)
            folder: the folder to save the json files to (defaults to current directory)
        '''
        for var in dicts:
            if var is 'portAnalCleaned':
                fileName = 'portAnalCleaned.json'
                data = self.portAnalCleaned

            elif var is 'perfDataCleaned':
                fileName = 'perfDataCleaned.json'
                data = self.perfDataCleaned

            elif var is 'portAnal':
                fileName = 'portAnal.json'
                data = self.portAnal

            elif var is 'perfData':
                fileName = 'perfData.json'
                data = self.perfData

            else:
                raise ValueError(f'Passed in invalid argument {var} to saveData().')

            with open(folder+fileName, mode='w') as out:
                json.dump(data, out)


if __name__ == '__main__':
    test = Portfolio()
    test.saveData()
