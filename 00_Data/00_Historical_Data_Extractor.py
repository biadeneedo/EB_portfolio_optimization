"""
# LIQUIDITY
# MEDIUM TO HIGH VOLATILITY
# GROUP FOLLOWERS (Contrarian Plays vs )

# MOST IMPORTANT INDEXES
# - S&P 500     --> 504 STOCKS
# - DOWN JONES  --> 30 STOCKS
# - NASDAQ 100  --> 100 STOCKS  
"""

import os
import yfinance as yf
import numpy as np
import pandas as pd

# Set wd
os.chdir(r'C:\Users\ebiadene\Documents\PROJECT_PROPOSAL\00_Financial_Markets\Algoritmic_Trading\00_Data')


# Get S&P500 tickers from a flat file
SP500 = pd.read_csv('00_S&P500_Tickers.csv', sep = ';')
SP500_Tickers = SP500['Symbol'].to_numpy()
print(SP500_Tickers)
tickers = SP500_Tickers
start_date = '2019-01-01'
end_date = '2020-01-01'

# Get S&P500 tickers from Wikipedia
# https://medium.com/python-data/how-to-scrape-information-of-s-p-500-listed-companies-with-python-8205f895ee7a 
data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
SP500table = data[0]
SP500tickers = SP500table['Symbol']




#################################################################################################################
#API CALLS
#################################################################################################################

#### TIINGO #####
# https://www.quandl.com/databases/AS500/documentation
import requests
symbol = ['MSFT', 'AAPL']

for i in SP500tickers:
    try:
        print (i)
        API_URL = "https://api.tiingo.com/tiingo/daily/{0}/prices".format(i) 
        #API_URL = "https://api.tiingo.com/iex/{0}/prices".format(symbol) #for intraday historical prices
        data = { "token": "bc6d085b32cb29574541ac4da54c8834a296b70b",
                'Content-Type': 'application/json',
                'startDate' : '2000-01-01',
                #'resampleFreq' : '1min'
                } 
        response = requests.get(API_URL, data) 
        response_json = response.json() # maybe redundant
        data = pd.DataFrame(response_json).sort_index(axis=1)
        data['date'] = data['date'].str[:10]
        data['ticker'] = i
        data.to_csv("SP500/{0}.csv".format(i), index = False, header=True, float_format='%.3f')
    except: 
        print ('error' + i) 


#### 1. YAHOO FINANCE ######
# tickers = ['AAPL', 'MSFT']
# df = yf.download(tickers,start_date,'2020-01-01')
df = pd.DataFrame(columns = ['Ticker','Data','Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
for i in tickers:
    foo = yf.download(i, start_date, end_date)
    print(foo.shape[0])
    foo['Ticker'] = i
    foo['Data'] = foo.index
    df = df.append(foo, ignore_index = True)

#### GOOGLEFINANCE ######
import googlefinance
panel_data = googlefinance.GOOGLEFINANCE(tickers, start_date, end_date)





#### QUANDL #####
# https://www.quandl.com/databases/AS500/documentation
import requests
API_URL = "https://www.quandl.com/api/v3/datasets/EOD/AAPL.json" 
symbol = 'MSFT'
data = { "api_key": "CRLdaxsq7WkWgy5t4FPB" } 

response = requests.get(API_URL, data) 
response_json = response.json() # maybe redundant
data = pd.DataFrame.from_dict(response_json['dataset'], orient= 'index').sort_index(axis=1)

data = response_json['dataset']
data = data['data']


import quandl
tickers = SP500_Tickers
#foo = quandl.get('WIKI/PRICES', api_key = "CRLdaxsq7WkWgy5t4FPB", ticker = tickers, start_date, end_date)
quandl.ApiConfig.api_key = 'CRLdaxsq7WkWgy5t4FPB'
data = quandl.get_table('WIKI/PRICES', ticker = ['AAPL', 'MSFT', 'WMT'], 
                        qopts = { 'columns': ['ticker', 'date', 'adj_close'] }, 
                        date = { 'gte': start_date, 'lte': end_date }, 
                        paginate=True)




##### ALPHAVANTAGE #####
# https://stackoverflow.com/questions/48071949/how-to-use-the-alpha-vantage-api-directly-from-python
# https://www.alphavantage.co/documentation/
import requests
API_URL = "https://www.alphavantage.co/query" 
symbol = 'MSFT'

data = { "function": "TIME_SERIES_DAILY_ADJUSTED", 
"symbol": symbol,
"outputsize" : "full",
"datatype": "json", 
"apikey": "JZ6EIIG5WCGWE3S8" } 

response = requests.get(API_URL, data) 
response_json = response.json() # maybe redundant

data = pd.DataFrame.from_dict(response_json['Time Series (Daily)'], orient= 'index').sort_index(axis=1)
data = data.rename(columns={ '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. adjusted close': 'AdjClose', '6. volume': 'Volume'})
data = data[[ 'Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']]
data.tail() # check OK or not


# THIS IS A WRAPPER 
from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key='JZ6EIIG5WCGWE3S8', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT',
                                  function = 'TIME_SERIES_DAILY_ADJUSTED',
                                  #interval='1min',
                                  outputsize='full')


#
alphav = __import__('01_AlphaVantage_Framework') # AlphaV relies on a external script
a=alphav.data('AlphaVantageApiKey') 
a.Outputsize='full'
a.Function='daily'
a.setSymbols('AIR.PAR,MC.PAR,FP.PAR,CS.PAR,EDF.PAR,AC.PAR,BNP.PAR,CAP.PAR,CA.PAR,ACA.PAR,BN.PAR,DSY.PAR,RMS.PAR,ENGI.PAR,OR.PAR,ORA.PAR,RNO.PAR,SAN.PAR,STM.PAR,HO.PAR,VIV.PAR')
a.bulkStream()
a.toCsv_UniqueVersion()



#################################################################################################################
# EXPORT RESULTS
#################################################################################################################

df.to_csv("00_db.csv", index = False, header=True)

