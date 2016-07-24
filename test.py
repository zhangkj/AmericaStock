
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade import dispatcher
from pyalgotrade import bar
from pyalgotrade.talibext import indicator
import os
import pandas as pd
import numpy as np
import datetime

print datetime.datetime.now()
print datetime.datetime.strptime("2016/03/10","%Y/%M/%d")


dataframe =nyse_df = pd.read_csv("data/nyse.csv")

dataframe[(dataframe.Sector=="Technology")&(dataframe.Industry=="Semiconductors")&(dataframe.LastSale> 20)]

dataframe["12"] = "12"
dat =[]
dat.append(dataframe[0:3])
dat.append(dataframe[3:5])

dataframe =pd.concat(dat)
dataframe.set_index("Symbol")

filename = "result/2016-04-17_download_data.csv"
df = pd.read_csv(filename)
df = df[(df.Date=="2016-04-15")&(df.Open<=20)&(df.Open>=10)&(df.Volume>=2000000)].sort_values(by="Open",ascending=False)
#print df[:10]
df = pd.concat([df[:5],df[-5:]])
#print df
#df.tocsv("test.csv")



#print dataframe["Symbol"]
def callback2(request, result):
    symbol = request.args[0]
    if result is not None:
        result[symbol] = symbol
        print result