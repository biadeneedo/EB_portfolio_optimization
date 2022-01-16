import os
import yfinance as yf
import numpy as np
import pandas as pd

# Set wd
os.chdir(r'C:\Users\ebiadene\Documents\PROJECT_PROPOSAL\00_Financial_Markets\Algoritmic_Trading\00_Data')

# Get S&P500 tickers from Wikipedia
# https://medium.com/python-data/how-to-scrape-information-of-s-p-500-listed-companies-with-python-8205f895ee7a 
data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
SP500table = data[0]
SP500tickers = SP500table['Symbol']


#################################################################################################################
#API CALLS
#################################################################################################################

#### ALPHAVANTAGE ####
import requests
API_URL = "https://www.alphavantage.co/query" 
symbol = 'A'

data = { "function": "OVERVIEW", 
"symbol": symbol,
#"outputsize" : "full",
#"datatype": "json", 
"apikey": "JZ6EIIG5WCGWE3S8" } 

response = requests.get(API_URL, data) 
response_json = response.json() # maybe redundant



#### TIINGO #####
import requests
symbol = ['MSFT', 'AAPL']

for i in symbol:
    try:
        print (i)
        API_URL = "https://cloud.iexapis.com/stable/stock/AAPL/earnings".format(i) 
        data = { "token": "sk_b1ed2169ca3b4c33a38fa0fbdfcd2dea",
                'startDate' : '2000-01-01'
                } 
        response = requests.get(API_URL, data) 
        response_json = response.json() # maybe redundant
        data = pd.DataFrame(response_json['earnings']).sort_index(axis=1)
        
        
        #data['date'] = data['date'].str[:10]
        #data['ticker'] = i
        #data.to_csv("SP500/{0}.csv".format(i), index = False, header=True, float_format='%.3f')
    except: 
        print ('error' + i) 

response.status_code


#### TIINGO #####
import requests
symbol = ['AMZN']

for i in symbol:
    try:
        print (i)
        API_URL = "https://api.tiingo.com/tiingo/fundamentals/'AAPL'/daily".format(i) 
        data = {"token": "bc6d085b32cb29574541ac4da54c8834a296b70b",
                'Content-Type': 'application/json',
                'startDate' : '2000-01-01'
                } 
        response = requests.get(API_URL, data) 
        response_json = response.json() # maybe redundant
        data = pd.DataFrame(response_json).sort_index(axis=1)
        data['date'] = data['date'].str[:10]
        data['ticker'] = i
        Enterprise_Value = data[['date', 'enterpriseVal', 'ticker']]
        Market_Cap = data[['date', 'enterpriseVal', 'ticker']]
        PB_Ratio = data[['date', 'pbRatio', 'ticker']]
        PE_Ratio = data[['date', 'peRatio', 'ticker']]
        PEG_1Y_trailing = data[['date', 'trailingPEG1Y', 'ticker']]
        Enterprise_Value.to_csv("SP500_Fundamental/{0}_Enterprise_Value.csv".format(i), index = False, header=True, float_format='%.3f')
        Market_Cap.to_csv("SP500_Fundamental/{0}_Market_Cap.csv".format(i), index = False, header=True, float_format='%.3f')
        PB_Ratio.to_csv("SP500_Fundamental/{0}_PB_Ratio.csv".format(i), index = False, header=True, float_format='%.3f')
        PE_Ratio.to_csv("SP500_Fundamental/{0}_PE_Ratio.csv".format(i), index = False, header=True, float_format='%.3f')
        PEG_1Y_trailing.to_csv("SP500_Fundamental/{0}_PEG_1Y_traling.csv".format(i), index = False, header=True, float_format='%.3f')
    except: 
        print ('error' + i) 

API_URL






