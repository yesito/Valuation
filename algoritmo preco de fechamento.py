# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import yfinance as yf
import pandas as pd

msft = yf.Ticker("HGTX3.SA")
data = msft.history(start ="2014-12-01",end = "2021-01-01")
data = data["Close"]

lst1 = []
close_p = []
datas = []
for i in range(len(data)-1,-1,-1):
    t = pd.Timestamp(data.index[i])
    d = t.date()
    mesey = (d.month, d.year)
    if mesey not in lst1:
        lst1 += [mesey]
        datas += [d.strftime("%d/%m/%Y")]
        close_p += [data[i]]
        print(data[i])
        
        
