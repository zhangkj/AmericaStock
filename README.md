# AmericaStock
统计美股近几年涨幅特别大的股票，在A股找到相关的股票

股票列表下载地址：http://www.nasdaq.com/screening/company-list.aspx

需要安装pyalgotrade pandas numpy


#myChange
1.对下载数据进行了调整，默认下载昨天数据，所有数据下载到一个csv文件中，并添加了symbol列；



#todo
1.爬取Finviz网站的数据；
2.对每日盘前新闻股，进行筛查，寻出观察交易股；
3.编写盘中检测程序，没5分钟进行一次筛查，选出有波动或突破的股；
全局股票监测：
1.全部价格交易量合适的股票进行监测;
2.对于创新高或步步走高的股票的进行筛选；
3.检测macd或MA金叉死叉发生的股票
4.
