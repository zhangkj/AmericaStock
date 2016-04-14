

import  pandas as pd


dataframe =nyse_df = pd.read_csv("data/nyse.csv")
dataframe["12"] = "12"
dat =[]
dat.append(dataframe[0:3])
dat.append(dataframe[3:5])

dataframe =pd.concat(dat)
print dataframe
def callback2(request, result):
    symbol = request.args[0]
    if result is not None:
        result[symbol] = symbol
        print result