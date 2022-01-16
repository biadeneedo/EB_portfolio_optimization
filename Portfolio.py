"""
# https://www.investopedia.com/articles/basics/11/5-portfolio-protection-strategies.asp
# DIVERSIFICATION - Icludes 10-30 stocks (Eliminate Unsystematic Risks)
# NON CORRELATING ASSET (Eliminate Systematic Risks)
# IDENTIFICARE UN TREND
# ANALIZZARE LE COSE PER SETTORE
# VOLATILITA'
# ESPOSIZIONE AI FATTORI DI RISCHIO
"""
import os
import pandas as pd
import numpy as np
import random
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from scipy import stats
#from sklearn.linear_model import LinearRegression
#from statsmodels.graphics.tsaplots import plot_acf

dir = r"C:\Users\ebiadene\OneDrive - Deloitte (O365D)\00_Project_Proposal\01_Financial_Markets\Algoritmic_Trading\00_Data\SP500_Historical"
os.chdir(dir+ '\..\..')
SP500info = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
LargeCap = pd.read_html('https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/') 

# IMPORTAZIONE DATI E CREAZIONE DIZIONARIO
d = {}
prova = []
for entry in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, entry)):
        d["{0}".format(entry)] = pd.read_csv(dir + '/' + entry)
        print(entry)
        prova.append(entry)

# CREAZIONE DATAFRAME RETURNS               
df_final = pd.DataFrame(columns=['ticker','slope','return_cum'])
df_close = pd.DataFrame(columns= ['ticker', 'date', 'close'])
df_return = pd.DataFrame(columns = ['ticker', 'date', 'return'])
df_return_cum = pd.DataFrame(columns = ['ticker', 'date', 'return_cum'])
df_logreturn = pd.DataFrame(columns = ['ticker', 'date', 'logreturn'])
df_logreturn_cum = pd.DataFrame(columns = ['ticker', 'date', 'logreturn_cum'])
for j in d.keys():     
    prova = d[j]
    prova = prova[prova['date'] >= '2019-01-01']
    prova['return'] = prova.close.pct_change()
    prova['return_cum'] = (prova['return'] + 1).cumprod()
    prova['logreturn'] = np.log(prova.close/prova.close.shift(1))
    prova['logreturn_cum'] = np.log(prova.close/prova.close.shift(1)).sum()
    prova['ticker'] = j.replace('.csv','') 
    Y = prova['date'].apply( lambda x : int( x.replace('-','') ))
    X = prova['close']
    slope, intercept, r_value, p_value, std_err = stats.linregress(Y, X)
    df = pd.DataFrame( {'ticker' : [j.replace('.csv','')], 'slope' : [slope], 'return_cum' : [prova['return_cum'].iloc[-1]]})
    df1 = prova[['ticker', 'date', 'close']]
    df2 = prova[['ticker', 'date', 'return']]
    df3 = prova[['ticker', 'date', 'return_cum']]
    df4 = prova[['ticker', 'date', 'logreturn']]
    df5 = prova[['ticker', 'date', 'logreturn_cum']]
    df_final = df_final.append(df)
    df_close = df_close.append(df1)
    df_return = df_return.append(df2)
    df_return_cum = df_return_cum.append(df3)
    df_logreturn = df_logreturn.append(df4)
    df_logreturn_cum = df_logreturn_cum.append(df5)
    d[j] = prova
    print(j)


# VISUALIZZAZIONE CURVE
fig = px.line(d['CARR.csv'], x='date', y='close')
fig.write_html('prova.html')


# CREAZIONE DB
stock_df = pd.merge(SP500info[['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry']], df_final,
                    left_on = 'Symbol', right_on = 'ticker')
Sector = stock_df.groupby('GICS Sector').mean()
Industry = stock_df.groupby('GICS Sub-Industry').mean()

df_close1 = pd.pivot(df_close.dropna(), index = 'date', columns = 'ticker', values = 'close')
df_logreturn= df_logreturn.reset_index()
df_logreturn1 = pd.pivot(df_logreturn.dropna(), index = 'date', columns = 'ticker', values = 'logreturn')
cov_matrix = df_logreturn1.cov() * 252



# PORFOLIO OTIMIZATION 
# Simulating 5000 portfolios
num_port = 5000
# Creating an empty array to store portfolio weights
all_wts = np.zeros((num_port, len(df_close1.columns)))
# Creating an empty array to store portfolio returns
port_returns = np.zeros((num_port))
# Creating an empty array to store portfolio risks
port_risk = np.zeros((num_port))
# Creating an empty array to store portfolio sharpe ratio
sharpe_ratio = np.zeros((num_port))

for i in range(num_port):
  #Setting random portfolio weights for each stock
  wts = np.random.uniform(size = 10)
  wts = wts/np.sum(wts)
  for j in wts:
      a = random.randint(0,493)
      all_wts[i,a] = j # saving weights in the array
  
  #Setting portolio returns based on logreturns and weights
  port_ret = np.sum(df_logreturn1.mean() * all_wts[i])
  port_ret = (port_ret + 1) ** 252 - 1
  port_returns[i] = port_ret # Saving Portfolio returns

  # Portfolio Risk
  port_sd = np.sqrt(np.dot(all_wts[i].T, np.dot(cov_matrix, all_wts[i])))
  port_risk[i] = port_sd
  
  # Portfolio Sharpe Ratio
  # Assuming 0% Risk Free Rate
  sr = port_ret / port_sd
  sharpe_ratio[i] = sr
  print(i)


names = df_close1.columns
min_var = all_wts[port_risk.argmin()]
print(min_var)

max_sr = all_wts[sharpe_ratio.argmax()]
print(max_sr)


import matplotlib.pyplot as plt
min_var = pd.Series(min_var, index=names)
min_var = min_var[(min_var.T != 0)]
min_var = min_var.sort_values()
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
ax1.set_xlabel('Asset')
ax1.set_ylabel("Weights")
ax1.set_title("Minimum Variance Portfolio weights")
min_var.plot(kind = 'bar')
plt.show();


max_sr = pd.Series(max_sr, index=names)
max_sr = max_sr[(max_sr.T != 0)]
max_sr = max_sr.sort_values()
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
ax1.set_xlabel('Asset')
ax1.set_ylabel("Weights")
ax1.set_title("Tangency Portfolio weights")
max_sr.plot(kind = 'bar')
plt.show();

fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
ax1.set_xlabel('Risk')
ax1.set_ylabel("Returns")
ax1.set_title("Portfolio optimization and Efficient Frontier")
plt.scatter(port_risk, port_returns)
plt.show();





