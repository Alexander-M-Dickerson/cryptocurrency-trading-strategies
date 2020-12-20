import requests
import pandas as pd
import numpy as np

# =============================================================================
# This script queries the CryptoCompare API and downloads data in panel form 
# for further analysis.
# =============================================================================

def coin_list():
    url = 'https://www.cryptocompare.com/api/data/coinlist/'
    page = requests.get(url)
    data = page.json()['Data']
    return data

coins = coin_list()
coin_tickers = list(coins.keys())

daily = pd.DataFrame()
coin = 0

# Insert your API key here #
api_key    = ""  

## Loop to download ALL cryptocurrency daily data ##
for coin in range(0,len(coin_tickers)):
    print(coin_tickers[coin] + str(coin))
    url = "https://min-api.cryptocompare.com/data/v2/histoday?fsym="+str(coin_tickers[coin])+\
        "&tsym=USD&limit=2000&e=CCCAGG&tryConversion=true"+\
          "&api_key="+str(api_key)
    f = requests.get(url)
    dat = f.json()
    if dat['Response'] == 'Success':        
        dat = dat['Data']
        dat = pd.DataFrame(dat['Data'])
        dat['ticker'] = str(coin_tickers[coin])
        dat['coin_name'] = coins[coin_tickers[coin]]['CoinName']
        daily = daily.append(dat)
    elif  dat['Response'] == 'Error':
        continue

daily.to_hdf(r'\CC_Data.h5', key='daily', mode='w')
