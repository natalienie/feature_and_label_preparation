import datetime
import time
import json
import urllib.request
import pandas as pd
import numpy as np
from TimeMachine import creatTimeStamp

def MACD(data):

    short_ave = data['close'].rolling(12).mean()
    long_ave = data['close'].rolling(26).mean()
    diff = short_ave - long_ave
    dea = diff.rolling(9).mean()
    macd = diff - dea
    return macd


def get_coin_data(currencyPair, start_date, end_date, hm_minute):
    '''
    currencyPair input form 'USDT_BCT, 'USDT_STR', ect
    start_date format : '2017-01-01'
    end_date format: '2018-01-01'
    hm_minute: how_many_minute input format should be int, 1 represent 1min ; 60 represent 1hour
    '''
    start_stamp = str(creatTimeStamp(start_date))
    end_stamp = str(creatTimeStamp(end_date))
    period = str(hm_minute * 60)

    url = 'https://poloniex.com/public?command=returnChartData&currencyPair=' + currencyPair + '&start=' + start_stamp + '&end=' + end_stamp + '&period=' + period
    data = urllib.request.urlopen(url)
    data = data.read().decode()
    data = json.loads(data)
    data1 = {'date': data['date'], 'close': data['close']}
    data1 = pd.DataFrame(data1)
    dates = np.array(data1['date'], dtype='datetime64[s]')
    data1['date'] = dates
    data1.set_index('date')
    macd = MACD(data1)
    data1['MACD'] = macd
    data1.dropna(axis=0, inplace=True)
    return data1

def creat_features_labels(data, magnitude, lag_window):
    '''
    each feature would be a one roll(one date), two columns(one column is price, one column is macd figure) data
    magnitude: input of an int, ie, 0.02(2%) is the desired percentage increase or decrease compared with current price.
    lag_window: input of an int, train the feature of macd & close price of one day, agaist the maximum value of the following N days or
    minimum value of the following N days. N is lag_window here
    is the maximum value of the follwing N days is > than (1+magnitue) * currentprice. which means price has gone up by 2%
    the label will be marked as 1
    if the minimu value of the following N days is < then (1-magnitude) * currentprice
    the label will be marked as -1
    else the label will be marked as 0
    '''
    label = []
    bar = 0
    x = len(data) - lag_window - 1
    features = data.iloc[:x]
    while bar < x:
        maxim = max(data['close'][bar+1: bar+lag_window])
        currentP = data['close'][bar]
        highmag = currentP * (1 + magnitude)
        lowmag = currentP * (1 - magnitude)
        minim = min(data['close'][bar+1: bar+lag_window])
        if maxim > highmag:
            label.append(1)
        elif minim < lowmag:
            label.append(-1)
        else:
            label.append(0)

    if len(features) != len(label):
        features = features[:len(label)]

    return features, label 
