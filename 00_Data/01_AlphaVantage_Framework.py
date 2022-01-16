import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import time
import datetime

class data:
    def __init__(self, mykey):
        
        self.Data=pd.DataFrame()       
        self.Outputsize='compact'
        self.Frequency='60min'        
        self.ts = TimeSeries(key=mykey, output_format='pandas')
        self.Function='daily'
        self.now=str(datetime.datetime.now().date())
        self.tickerlist=[]
        self.tickerSetByUser=0
        self.separator=','    
       
    def get(self,ticker):
        
        if self.Function=='intraday':    
             _data, meta_data = self.ts.get_intraday(symbol=ticker\
             ,interval=self.Frequency,outputsize=self.Outputsize)            
             
        elif self.Function=='daily':
             _data, meta_data = self.ts.get_daily(symbol=ticker\
             ,outputsize=self.Outputsize)    
             
        _data.columns=['open', 'high','low','close','volume']   
        _data['ticker']=ticker        
        self.Data=self.Data.append(_data)
    
    def _bulkStream(self,_tickerlist):        
        print('Starting Bulk Download: \n')        
        print(_tickerlist)        
        print('\n')
        for i in range(len(_tickerlist)):
            if i!=0 and i%5==0:
                print("_________________\n")
                time.sleep(60)                    
            
            self.get(_tickerlist[i])
            print(str(i)+'.  '+_tickerlist[i])
            
    def bulkStream(self):
        if self.tickerSetByUser==1:
            _tickerlist=self.tickerlist.split(self.separator)
            self._bulkStream(_tickerlist)
        
        elif self.tickerSetByUser==2:
            _tickerlist= self.tickerlist
            self._bulkStream(_tickerlist)    
            
    def toCsv(self):
        self.Data.to_csv('DataExport_'+self.now+'.csv')       
    
    def toCsv_UniqueVersion(self):
        self.Data.to_csv('DataExport.csv')       
    
    def importSymbols(self,path,columnName):
        self.tickerSetByUser=2        
        df=pd.read_csv(path)
        self.tickerlist=df[columnName].tolist()
        
    def setSymbols(self, tickerstring):
        self.tickerSetByUser=1
        self.tickerlist=tickerstring
        


