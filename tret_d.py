# -*- coding: utf-8 -*-
"""
Created on Sun May  7 12:31:15 2023

@author: kacem
"""
import datetime
import pandas as pd
import MetaTrader5 as mt5

item = "BTCUSD"


# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
 
# request connection status and parameters
print(mt5.terminal_info())
# get data on MetaTrader 5 version
print(mt5.version())


btc_rates = mt5.copy_rates_from_pos(item, mt5.TIMEFRAME_D1, 0, 1000)


rates_frame = pd.DataFrame(btc_rates)
# convert time in seconds into the datetime format
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

rates_frame['diff'] =  (rates_frame['close'] - rates_frame['open']) / rates_frame['open']


file_name = item
rates_frame.to_csv("C:/Users/kacem/OneDrive/Bureau/D/diff_data/" + file_name, sep=',')

mt5.shutdown()