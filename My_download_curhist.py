#-*-encoding:utf-8-*-
'''
download  history data

'''

from pyalgotrade.tools import yahoofinance
from pyalgotrade.utils import dt
import threadpool
import pandas as pd
import datetime

global DATA,BEGIN,END,Market

#读取全部市场stock为datastocklist内容
def getAllStockData(beginDate, endDate):
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
    #begin =  datetime.date(year, month, day) - datetime.timedelta(days=7)
    #end = datetime.date(year, month, day) - datetime.timedelta(days=1)
    begin = beginDate
    end = endDate
    #------symbol设置
    #data = nasdaq_df['Symbol'].tolist() + amex_df['Symbol'].tolist()+nyse_df['Symbol'].tolist()
    global  DATA
    DATA = nyse_df['Symbol'][:].tolist()
    print DATA,begin,end

#设置datastocklist数据指定文件内容
def getSpecialStockList(fileName):
     stockList = pd.read_csv(fileName)
     global  DATA
     DATA = stockList['Symbol'].tolist()

def ExportResult(result):
    csvFile = "result/"+str(END) + "%s.csv" % ("_download_data_"+Market)
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
        print str(len(DATA)) + "index;" + str(index)

def callback(request, result):
    symbol = request.args[0]
    csvFile = "result/%s.csv"%(symbol)
    if result is not None:
        f = open(csvFile, "w")
        f.write(result)
        f.close()

def run(symbol):
    try:
        return yahoofinance.download_csv(symbol, BEGIN, END, "d")
    except Exception:
        pass

def main():
    global  BEGIN,END,Market
    BEGIN = datetime.date(2016,6,24)
    END = datetime.date(2016,6,24)
    Market = "nasdaq"
    print BEGIN,END,Market
    #getAllStockData(begin, end)
    getSpecialStockList("data/"+Market+".csv")
    thread_num = 100
    pool = threadpool.ThreadPool(thread_num)
    requests = threadpool.makeRequests(run, DATA, callback2)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    pool.dismissWorkers(thread_num, do_join=True)

    ExportResult(resultlist)
if __name__ == '__main__':
    main()


#yahoofinance.download_weekly_bars(instrument, year, csvFile)