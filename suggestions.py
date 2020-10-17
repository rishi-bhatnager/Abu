import json
import requests

# sp500financials will be a list of 505 dictionaries
# NOTE: THIS DATA IS 3 MONTHS OLD (source: https://datahub.io/core/s-and-p-500-companies-financials#python)
url = 'https://pkgstore.datahub.io/core/s-and-p-500-companies-financials/constituents-financials_json/data/ddf1c04b0ad45e44f976c1f32774ed9a/constituents-financials_json.json'
sp500financials = requests.get(url).json()


# a dict that maps to a dict that maps the ticker to each data point in the json individually
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
    '''
