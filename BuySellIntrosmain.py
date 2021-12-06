import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
#matplotlib is a library; we're using the pyplot subset of the library
#as 'plt' to refer to the plotchart that we can create using the library

plt.style.use('fivethirtyeight')
#We're using the style of fivethirtyeight.com, the website that produces
#political poll data
pd.set_option('display.max_columns', None)

datasource = 'SPY.csv'
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



#Now, lets use some data like last week and calculate our RSI
#To skip the review, head straight to line 52
datasource = 'SPY.csv'
df = pd.read_csv(datasource)
#calculate RSI
rsi_interval = 14
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
avg_gain = gain.ewm(com = rsi_interval - 1,min_periods = rsi_interval).mean()
avg_loss = loss.ewm(com = rsi_interval - 1,min_periods = rsi_interval).mean()
rs = abs(avg_gain/avg_loss)
rsi = 100 - (100/(1+rs))
df['rsi'] = rsi
#print(df.head())
#print(df.tail())


#Now create a function that creates buy and sell signals based off the stipulations of oversold and overbought 
#of the RSI indicator
#after that you will plot a graph that has the underlying asset/stock price, the RSI, and the arrow ticks
#that show where to buy and sell on the data given

dataToUse = pd.DataFrame()
dataToUse['Close Prices'] = df['Adj Close']
dataToUse['RSI'] = df['rsi']

#make the function def buy_sell() that takes in a paramater of a csv file
def buy_sell(data):
  sigPriceBuy=[]
  sigPriceSell=[]
  flag = -1 #we will use this to note if we've bought (1), sold (0).

  for i in range(len(data)):
    if data['RSI'][i]<= 30: #We've pyhtofound an RSI < 30, a buy signal
      if flag!=1:  #Have we bought yet?  If not...
        sigPriceBuy.append(data['Close Prices'][i]) #at index i, store the price of SPY at this point where we found the buy signal

        sigPriceSell.append(np.nan) #In the sell column, fill a blank NaN
        flag = 1 #Set the flag to 1 to indicate that we've bought, waiting to sell
      
      else: #If we've already bought/entered the position...
        sigPriceSell.append(np.nan) #fill both the buy/sell charts with NaN
        sigPriceBuy.append(np.nan)

    elif data['RSI'][i]>=70: #We've found an RSI > 70, a sell signal
      if flag !=0: #Have we bought and are waiting to sell? If so
        sigPriceSell.append(data['Close Prices'][i]) #At index i, where i is this day where RIS > 70, we log the price of SPY on this day
        sigPriceBuy.append(np.nan)
        flag = 0
      else:
        sigPriceSell.append(np.nan)
        sigPriceBuy.append(np.nan)
    else:
      sigPriceSell.append(np.nan)
      sigPriceBuy.append(np.nan)
      
  return (sigPriceBuy,sigPriceSell) #return the list of buy prices and sell prices


'''
Our RSI, Buy Signal, and sell charts will look like this:
For the csv we're using, each line is one day. So each index/cell in our
list is the data for one day
     Day1 Day2 ....Day4   .......      Day9
        V   V       V                   V
rsi:  [45, 32, 28, 31, 36, 29, 33, 40, 60, 65, 71, 69, 70, ..... , 35, 30]
Buy:  [Nan, N,  B,  N,  N,  N,  N,  N,  N,  N,  N,  N  N,   ....... N,  B]
Sell: [an,  N,  N,  N,  N,  N,  N,  N,  N,  N,  S,  N, N, ......    N,  N]
                |                               |                       |
      Here, we Buy, wait to sell     Here, we sell, wait to buy        Buy

Wherever we have a B or an S, we want to record the price on that day

Why? Because then we can plot the list, using the indices as x values, and the price of the stock on that day as y values (each index is 1 day, in order)

using this, we can slap the graph of buy points and sell points on top
of the stock chart, where the stock chart also uses the x values as days
'''

buySell = buy_sell(dataToUse) # returns a tuple of the buy signals, sell signals
dataToUse['Buy Signal Price'] = buySell[0] #add a column of buy signals
dataToUse['Sell Signal Price'] = buySell[1] #add a column of sell signals
print(dataToUse['Sell Signal Price'].head(70)) 
#now we have where the buy and sell signals are so now we will plot them



#We got our data! Now, lets use our plt library from line 4/5 to visualize it
#set a range of our figure 
plt.figure(figsize = (10,3))

#start off by plotting the price of $SPY over time
plt.plot(dataToUse['Close Prices'], label='SPY',alpha = 0.35)
# the .plot() function takes parameters for a list of data points, a label, and an adjusted alpha value 


#scatter the sell signal points, lebeling them 'sell', using v for the points, and coloring them red
plt.scatter(dataToUse.index, dataToUse['Sell Signal Price'], label='Sell', marker='v',color='red')

#scatter the buy signal points, labeled 'buy', using ^ and coloring them green
plt.scatter(dataToUse.index, dataToUse['Buy Signal Price'], label='Buy', marker='^',color='green')

#title the graph
plt.title('SPY Adjusted Close RSI Buy and Sell Signals')

#Set a label for the x axis
plt.xlabel('8 April 2020 - 7 April 2021')

#Set a label for the y axis
plt.ylabel('Adj Close Price SPY $USD')

#Create a legend for the graph, and set the location (loc) to the upper left corner
plt.legend(loc='upper left')

#show the graph that we've designed!
plt.show()




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


