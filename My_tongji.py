
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade import dispatcher
from pyalgotrade import bar
from pyalgotrade.talibext import indicator
import os
import pandas as pd
import numpy as np
from datetime import datetime

filenames  =  os.listdir("result")
changeprice = "changeprice"
changepercent = "changepercent(%)"
rchangepercent = "rchangepercent(%)"
close = "Close"
open = "Open"
high = "High"
low = "Low"
adjClose = "Adj Close"
for filename in filenames:
    symbol = os.path.splitext(filename)[0]
    df = pd.read_csv("result/%s"%(filename))
    df = df.sort_values(by="Date")
    df = df.set_index("Symbol")
    df =  df.reindex(columns=list(df.columns)[:]+[changeprice,changepercent,rchangepercent])

    df.loc[:,changepercent] = ((df[close]-df[open])/df[open]*100).round(2)
    df.loc[:,rchangepercent] = ((df[close]-df[open])/df[open]).round(2)
    df.loc[:,changeprice] = (df[close]-df[open]).round(2)

    df = df.sort_values(by=changepercent,ascending=False)

df.to_csv("data/my_tongji_result.csv")
#barFeed.setUseAdjustedValues(True)
'''
dispatcher = dispatcher.Dispatcher()
dispatcher.addSubject(barFeed)
dispatcher.run()

for filename in filenames[0:100]:
    symbol = os.path.splitext(filename)[0]
    closeDS = list(barFeed.getDataSeries(symbol).getAdjCloseDataSeries())
    max_v = max(closeDS)
    max_v_index = closeDS.index(max_v)
    if max_v_index == 0:
        continue
    min_v = min(closeDS[:max_v_index])
    print symbol,min_v,max_v
'''

            



