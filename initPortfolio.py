# pre-loads the data set and allows for custom url creation

import json, requests

class Portfolio:
    def __init__(self, holdings={'AAPL': 150,'TSLA': 50,'SPY': 100}, usePortAnal=True):
        self.holdings = holdings
        portfolio_anlaysis = 'https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExpectedReturns=true& \
            calculateExposures=true&calculatePerformance=true&calculateRisk=true&includeChartData=true&positions='
        performance_data ='https://www.blackrock.com/tools/hackathon/performance?identifiers='

        for ticker,shares in holdings.items():
            portfolio_anlaysis += f'{ticker}~{str(shares)}%7C'
            performance_data += ticker + '%2C'

        portfolio_anlaysis = portfolio_anlaysis[:-3]
        performance_data = performance_data[:-3]

        if usePortAnal:
            self.portAnal = requests.get(portfolio_anlaysis).json()
            self.portAnalCleaned = self.portAnal['resultMap']['PORTFOLIOS'][0]['portfolios'][0]

        self.perfData = requests.get(performance_data).json()
        self.perfDataCleaned = self.perfData['resultMap']['RETURNS']


    def saveData(self, dicts=[('portAnalCleaned', 'portAnalCleaned.json'), ('perfDataCleaned', 'perfDataCleaned.json')], folder='./'):
        '''
        Saves the given data as a json file into the specified folder

        Params:
            dicts: length-2 tuples containing string representataions of the names of the dictionaries to save
                (defaults to the cleaned data from both APIs) and preferred file names (in that order)
            folder: the folder to save the json files to (defaults to current directory)
        '''
        for var,name in len(dicts):
            if var is 'portAnalCleaned':
                fileName = name
                data = self.portAnalCleaned

            elif var is 'perfDataCleaned':
                fileName = name
                data = self.perfDataCleaned

            elif var is 'portAnal':
                fileName = name
                data = self.portAnal

            elif var is 'perfData':
                fileName = name
                data = self.perfData

            else:
                raise ValueError(f'Passed in invalid argument {var} to saveData().')

            if not fileName.endswith('.json'):
                raise ValueError(f'File name must end in .json! File name received: {fileName}')

            with open(folder+fileName, mode='w') as out:
                json.dump(data, out)


    def __str__():
        return self.holdings

    def __repr__():
        return __str__()



if __name__ == '__main__':
    test = Portfolio()
    test.saveData()
