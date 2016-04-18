#-*-encoding:utf-8-*-
"""
tongji data
"""



from pyalgotrade.barfeed import yahoofeed
from pyalgotrade import dispatcher
from pyalgotrade import bar
from pyalgotrade.talibext import indicator
import os
import pandas as pd
import numpy as np
import datetime

now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day


fileDate = datetime.date(year,month,day-1)
dataDirName = "result/"
tongji_fileName= str(fileDate) + "_tongji_Result.csv"
downloadData_fileName = str(fileDate)+"_download_data.csv"
tongji_data_fileName = str(fileDate)+"_tongji_data.csv"
tongji_ChangeTop_fileName = dataDirName + str(fileDate)+"_DayChangeTop10.csv"  #上一交易日波动top10
dataFile = "result/"+downloadData_fileName
exportFile = "result/"+ tongji_fileName
exportTongjiFile = "result/"+ tongji_data_fileName


changeprice = "changeprice"
changepercent = "changepercent(%)"
rchangepercent = "rchangepercent(%)"
close = "Close"
open = "Open"
high = "High"
low = "Low"
adjClose = "Adj Close"
Symbol = "Symbol"

incrMonth4 = "incrMonth4(%)"





#添加列，并计算changeprice、changepercent、rchangepercent
def calculate(df):
    df = df.set_index(Symbol)
    df =  df.reindex(columns=list(df.columns)[:]+[changeprice,changepercent,rchangepercent])

    df.loc[:,changepercent] = ((df[close]-df[open])/df[open]*100).round(2)
    df.loc[:,rchangepercent] = ((df[close]-df[open])/df[open]).round(2)
    df.loc[:,changeprice] = (df[close]-df[open]).round(2)

    df = df.sort_values(by=changepercent,ascending=False)
    df.to_csv(exportFile)

indexSymbol = 0
def tongjiData(df):
    #nasdaq
    nasdaq_df = pd.read_csv("data/nasdaq.csv")
    nasdaq_df = nasdaq_df[nasdaq_df.Industry != 'n/a']

    #amex
    amex_df = pd.read_csv("data/amex.csv")
    amex_df = amex_df[amex_df.Industry != 'n/a']

    #ntse
    nyse_df = pd.read_csv("data/nyse.csv")
    nyse_df = nyse_df[nyse_df.Industry != 'n/a']

    #stock_list_df = pd.concat([nasdaq_df,amex_df,nyse_df])
    stock_list_df = pd.concat([nyse_df])
    stock_list_df = stock_list_df.drop_duplicates('Symbol')
    stock_list_df = stock_list_df.set_index("Symbol")

    stock_list_df = stock_list_df.reindex(columns=list(stock_list_df.columns)[:]+[incrMonth4,'incr2016','incr2015','incr2014','incr2013','incr3year','incr6year'])
    for symbol in stock_list_df.index:
        try:
            global  indexSymbol
            indexSymbol+=1
            print str(len(stock_list_df.index))+"index;" + str(indexSymbol)
            symbol_df = df[df[Symbol]==symbol]
            qoute_month4_df = symbol_df[(symbol_df['Date']>='2016-04-01') & (symbol_df['Date']<'2016-05-01')].reset_index()
            qoute_2015_df = symbol_df[(symbol_df['Date']>'2014-12-31') & (symbol_df['Date']<'2016-01-01')].reset_index()
            qoute_2014_df = symbol_df[(symbol_df['Date']>'2013-12-31') & (symbol_df['Date']<'2015-01-01')].reset_index()
            qoute_2013_df = symbol_df[(symbol_df['Date']>'2012-12-31') & (symbol_df['Date']<'2014-01-01')].reset_index()
            qoute_3year_df = symbol_df[(symbol_df['Date']>'2012-12-31') & (symbol_df['Date']<'2016-01-01')].reset_index()
            qoute_6year_df = symbol_df[(symbol_df['Date']>'2009-12-31') & (symbol_df['Date']<'2016-01-01')].reset_index()
            if not qoute_month4_df.empty:
                stock_list_df.loc[symbol,incrMonth4] = round((qoute_month4_df['Adj Close'][len(qoute_month4_df['Adj Close'])-1] - qoute_month4_df['Adj Close'][0])/qoute_month4_df['Adj Close'][0]*100,2)
            if not qoute_2015_df.empty:
                stock_list_df.loc[symbol,'incr2015'] = round((qoute_2015_df['Adj Close'][len(qoute_2015_df['Adj Close'])-1] - qoute_2015_df['Adj Close'][0])/qoute_2015_df['Adj Close'][0]*100,2)
            if not qoute_2014_df.empty:
                stock_list_df.loc[symbol,'incr2014'] = round((qoute_2014_df['Adj Close'][len(qoute_2014_df['Adj Close'])-1] - qoute_2014_df['Adj Close'][0])/qoute_2014_df['Adj Close'][0]*100,2)
            if not qoute_2013_df.empty:
                stock_list_df.loc[symbol,'incr2013'] = round((qoute_2013_df['Adj Close'][len(qoute_2013_df['Adj Close'])-1] - qoute_2013_df['Adj Close'][0])/qoute_2013_df['Adj Close'][0]*100,2)
            if not qoute_3year_df.empty:
                stock_list_df.loc[symbol,'incr3year'] = round((qoute_3year_df['Adj Close'][len(qoute_3year_df['Adj Close'])-1] - qoute_3year_df['Adj Close'][0])/qoute_3year_df['Adj Close'][0]*100,2)
            if not qoute_6year_df.empty:
                stock_list_df.loc[symbol,'incr6year'] = round((qoute_6year_df['Adj Close'][len(qoute_6year_df['Adj Close'])-1] - qoute_6year_df['Adj Close'][0])/qoute_6year_df['Adj Close'][0]*100,2)
        except:
            continue
    stock_list_df = stock_list_df[stock_list_df[incrMonth4].notnull()]
    stock_list_df.to_csv(exportTongjiFile)

def selectChangeTop10():
    df = pd.read_csv(exportFile)
    df = df[(df.Date=="2016-04-15")&(df.Open<=20)&(df.Open>=10)&(df.Volume>=2000000)]
    df  = pd.concat([df[:10],df[-10:]])
    df.to_csv(tongji_ChangeTop_fileName)


def main():
    if  os.path.exists(dataFile):
        df = pd.read_csv(dataFile)
        df = df.sort_values(by="Date")
        calculate(df)
        selectChangeTop10()
        #tongjiData(df)
    else:
        print dataFile + " not exist."

            
if __name__ == "__main__":
    main()


