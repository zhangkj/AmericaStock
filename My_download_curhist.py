#-*-encoding:utf-8-*-
'''
download  history data

'''

from pyalgotrade.tools import yahoofinance
from pyalgotrade.utils import dt
import threadpool
import pandas as pd
import datetime


#nasdaq
nasdaq_df = pd.read_csv("data/nasdaq.csv")
nasdaq_df = nasdaq_df[nasdaq_df.Industry != 'n/a']

#amex
amex_df = pd.read_csv("data/amex.csv")
amex_df = amex_df[amex_df.Industry != 'n/a']

#ntse

nyse_df = pd.read_csv("data/nyse.csv")
nyse_df = nyse_df[nyse_df.Industry != 'n/a']

now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day

#-------时间区间设置
begin =  datetime.date(year, month, day) - datetime.timedelta(days=14)
end = datetime.date(year, month, day) - datetime.timedelta(days=1)
#------symbol设置
#data = nasdaq_df['Symbol'].tolist() + amex_df['Symbol'].tolist()+nyse_df['Symbol'].tolist()
data = nyse_df['Symbol'][:10].tolist()
print data,begin,end



def ExportResult(result):
    csvFile = "result/"+str(end)+"%s.csv"%("_download_data")
    if result is not None:
        f = open(csvFile, "w")
        f.write(result)
        f.close()

resultlist = ''
index = 0
def callback2(request, result):
    symbol = request.args[0]
    if result is not None:
        global  resultlist,index
        if index==0:
            resultlist += "Date,Open,High,Low,Close,Volume,Adj Close,Symbol\n"
            resultlist += result[42:].replace('\n',','+str(symbol)+'\n')
        else:
            resultlist += result[42:len(result)].replace('\n',','+str(symbol)+'\n')
        index+=1
        print str(len(data))+"index;" + str(index)

def callback(request, result):
    symbol = request.args[0]
    csvFile = "result/%s.csv"%(symbol)
    if result is not None:
        f = open(csvFile, "w")
        f.write(result)
        f.close()

def run(symbol):
    try:
        return yahoofinance.download_csv(symbol,begin, end, "d")
    except Exception:
        pass
thread_num = 100
pool = threadpool.ThreadPool(thread_num)
requests = threadpool.makeRequests(run, data, callback2)
[pool.putRequest(req) for req in requests]
pool.wait()
pool.dismissWorkers(thread_num, do_join=True)

ExportResult(resultlist)

#yahoofinance.download_weekly_bars(instrument, year, csvFile)