import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')



pd.set_option('display.max_columns', None)
datasource = 'AMD.csv'
df = pd.read_csv(datasource)

#calculate RSI

rsi_period = 14

#diff(1) is over what period of days the difference is calculated
change = df['Adj Close'].diff(1)

#non gain (loss) is replaced with 0 because no gain
gain = change.mask(change < 0, 0)
#df['gain'] = gain

#we do the same for the loss
loss = change.mask(change > 0, 0)
#df['loss'] = loss

#typically we dont show these loss and gain columns but for learning purposes we do

#next calculate average gain and losses
avg_gain = gain.ewm(com = rsi_period - 1,min_periods = rsi_period).mean()
avg_loss = loss.ewm(com = rsi_period - 1,min_periods = rsi_period).mean()

rs = abs(avg_gain/avg_loss)
rsi = 100 - (100/(1+rs))

df['rsi'] = rsi

#print(df.head())
#print(df.tail())




#Now create a function that creates buy and sell signals based off the stipulations of oversold and overbought 
#of the RSI indicator
#after that you will plot a graph that has the underlying asset/stock price, the RSI, and the arrow ticks
#that show where to buy and sell on the data given

#make the function def buy_sell() that takes in a paramater of a csv file

dataToUse = pd.DataFrame()
dataToUse['SPY Close Prices'] = df['Adj Close']
dataToUse['RSI'] = df['rsi']

def buy_sell(data):
  sigPriceBuy=[]
  sigPriceSell=[]
  flag = -1 #we will use this to note if weve been here

  for i in range(len(data)):
    if data['RSI'][i]<= 30:
      if flag!=1:
        sigPriceBuy.append(data['SPY Close Prices'][i])
        sigPriceSell.append(np.nan)
        flag = 1
      else:
        sigPriceSell.append(np.nan)
        sigPriceBuy.append(np.nan)
    elif data['RSI'][i]>=70:
      if flag !=0:
        sigPriceSell.append(data['SPY Close Prices'][i])
        sigPriceBuy.append(np.nan)
        flag = 0
      else:
        sigPriceSell.append(np.nan)
        sigPriceBuy.append(np.nan)
    else:
      sigPriceSell.append(np.nan)
      sigPriceBuy.append(np.nan)
      
  return (sigPriceBuy,sigPriceSell)




buySell = buy_sell(dataToUse)
dataToUse['Buy Signal Price'] = buySell[0]
dataToUse['Sell Signal Price'] = buySell[1]
print(dataToUse['Sell Signal Price'].head(70))
#now we have where the buy and sell signals are so now we will plot them

plt.figure(figsize = (10,3))
plt.plot(dataToUse['SPY Close Prices'], label='SPY',alpha = 0.35)
plt.scatter(dataToUse.index, dataToUse['Sell Signal Price'], label='Sell', marker='v',color='red')
plt.scatter(dataToUse.index, dataToUse['Buy Signal Price'], label='Buy', marker='^',color='green')
plt.title('SPY Adjusted Close RSI Buy and Sell Signals')
plt.xlabel('8 April 2020 - 7 April 2021')
plt.ylabel('Adj Close Price SPY $USD')
plt.legend(loc='upper left')
plt.show()




buySell = buy_sell(dataToUse)
dataToUse['Buy Signal Price'] = buySell[0]
dataToUse['Sell Signal Price'] = buySell[1]
print(dataToUse['Sell Signal Price'].head(70))
#now we have where the buy and sell signals are so now we will plot them

plt.figure(figsize = (10,3))
plt.plot(dataToUse['SPY Close Prices'], label='SPY',alpha = 0.35)
plt.scatter(dataToUse.index, dataToUse['Sell Signal Price'], label='Sell', marker='v',color='red')
plt.scatter(dataToUse.index, dataToUse['Buy Signal Price'], label='Buy', marker='^',color='green')
plt.title('SPY Adjusted Close RSI Buy and Sell Signals')
plt.xlabel('8 April 2020 - 7 April 2021')
plt.ylabel('Adj Close Price SPY $USD')
plt.legend(loc='upper left')
plt.show()


