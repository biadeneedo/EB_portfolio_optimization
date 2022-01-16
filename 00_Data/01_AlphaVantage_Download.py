# LIQUIDITY
# MEDIUM TO HIGH VOLATILITY --> determine high VIX and a Beta > 1 
#                               (that means stocks is more volatile than the corrispindent index)
# GROUP FOLLOWERS (Contrarian Plays vs )

import os
import numpy as np
import pandas as pd

os.chdir('C:\\Users\\ebiadene\\Documents\\PROJECT_PROPOSAL\\00_Financial Markets\\00_Data')

# S&P 500 db
db = pd.read_csv("00_db.csv")






# ALPHAVANTAGE
alphav = __import__('01_AlphaVantage_Framework') # AlphaV relies on a external script
a=alphav.data('AlphaVantageApiKey') 
a.Outputsize='full'
a.Function='daily'
a.setSymbols('AIR.PAR,MC.PAR,FP.PAR,CS.PAR,EDF.PAR,AC.PAR,BNP.PAR,CAP.PAR,CA.PAR,ACA.PAR,BN.PAR,DSY.PAR,RMS.PAR,ENGI.PAR,OR.PAR,ORA.PAR,RNO.PAR,SAN.PAR,STM.PAR,HO.PAR,VIV.PAR')
a.bulkStream()
a.toCsv_UniqueVersion()
