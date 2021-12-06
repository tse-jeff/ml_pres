import pandas as pd
import statsmodels.api as sm
import yfinance as yf
from datetime import datetime
import yahoo_fin.options as ops
import json

class Deliverable:
  def __init__ (self, ticker, since_date):
    self.ticker, self.since_date = ticker, since_date
    self.predicted_x_df = []

  def BasicExpectations(StartPeriod, EndPeriod, ColName, DF):
    sum=0
    for StartPeriod in range(EndPeriod):
        sum=sum+DF[ColName][EndPeriod]
    return sum/(EndPeriod-StartPeriod)

  # def train_multivariate_model(self, df):
  #     # create multiple regression model with all independent variables (use statsmodel.api)
  #   x = df.drop(columns=['Stock_Price'])
  #   y = df['Stock_Price']

  #   self.multi_model = sm.OLS(y,x).fit()

  #   print(self.multi_model.summary())
  #   print(self.multi_model.params)

  #   pass


  def get_timeseries_model(self):
    # do simple regression with independent variable as the y and time as the x (so that we can get the next unknown value of the independent variable)

		# for
    pass


  def get_prediction(self):
    # using the next values for each independent variable (via timeseries models), predict tomorrow's stock price by plugging those values into multiple regression model
    pass


  # get Close price and Volume from yahoo finance api
  # returns dataframe with 'Close' and 'Volume' columns
  def fetch_stock_data(self, ticker, volume=True):
    # use yfinance
    # TODO: catch error if invalid symbol entered
    ticker_obj = yf.Ticker(ticker)
    history = ticker_obj.history(start=self.since_date, end=datetime.today(), interval="1d")
    history = history.drop(['Open', 'High', 'Low', 'Dividends', 'Stock Splits'], axis=1)
    # TODO: DJI index does have volume data; check if volume column is not 0's instead of index flag if we want to use that as a predictor?
    if not volume:
      history = history.drop(['Volume'], axis=1) # no volume for VIX index
    history = history.rename(lambda col: ticker + " " + col, axis='columns')
    # print("[DEBUG] yfinance data for $" + ticker)
    # print(history.head())
    # print("---------------------------------/>")
    return history

  def fetch_option_data(self):
    # options data
    # NOTE: need to find a better source for historial option data; yfinance only allows you to fetch 'current' data for future strike dates
    # call_options = pd.DataFrame()
    # put_options = pd.DataFrame()
    # get options chain for first 10 strike dates (could do a specific period of time in the future instead)
    # for i in range(0, 10):
    #   option_chain = ticker_obj.option_chain(date=ticker_obj.options[i])
    #   call_options = call_options.append(option_chain.calls, ignore_index=True)
    #   put_options = put_options.append(option_chain.puts, ignore_index=True)
    pass


  def fetch_treasury_yields(self):
    r = requests.get('https://www.quandl.com/api/v3/datasets/USTREASURY/YIELD.json?api_key=gdtyN_LzUGFrZuqwP3zn')
    tmp = pd.DataFrame(json.loads(r.content)['dataset']['data']) 
    self.main_df["1 MO","2 MO","3 MO","6 MO","1 YR","2 YR","3 YR","5 YR","7 YR","10 YR","20 YR","30 YR"] = tmp.iloc[0:list(tmp[0]).index(self.since_date),1:]


  def run(self):
    ## here is an alternative implementation of Clenaing the Vix and DJI data 
    # VIX = yf.Ticker("VIX")
    # Vix_df = VIX.history(period="max")
    # VIX_df=Vix_df.drop(['Open', 'High', 'Low', 'Dividends', 'Stock Splits'],axis=1).rename(columns={"Close": "Vix Close", "Volume": "Vix Volume"})
    # DJI = yf.Ticker("DJI")
    # DJI_df = DJI.history(period="max")
    # DJI_df=DJI_df.drop(['Open', 'High', 'Low', 'Dividends', 'Stock Splits'],axis=1).rename(columns={"Close": "DJI Close", "Volume": "DJI Volume"})
    # VIXandDJI = pd.concat([DJI_df, VIX_df], axis=1)


    stock_df = self.fetch_stock_data(self.ticker)
    vix_df = self.fetch_stock_data("^VIX", False)
    dji_df = self.fetch_stock_data("^DJI")
    self.fetch_treasury_yields()
    # bond_df = self.fetch_bond_yields()

    self.main_df = pd.concat([stock_df, vix_df, dji_df], axis=1)
    print(self.main_df)

	# train_multivariate_model(self.main_df)
  
  def gather_options_data():
    pass


stockSymbol = input("Enter a Stock Symbol traded on a U.S Market (CBOE/BATS, NASDAQ, NYSE): ").upper()
application = Deliverable(stockSymbol, "2021-04-01")
application.run()

