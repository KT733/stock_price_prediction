# Functions for calculating technical indicators

## function that calculates moving average
def MA_calculation(ticker,MAs = [5,10,20,50,100,200,500]):
    """
    Create moving average columns of 'close'
    data column in our historical price dataset
    """
    ticker = ticker.copy()
    for ma in MAs:
        ticker[f'MA_{ma}'] = ticker['Close'].rolling(window=ma,min_periods=1).mean()
    return ticker

## function that calculates Moving average convergence divergence (MACD)
def MACD_calculation(ticker):
    ticker=ticker.copy()
    # Get the 26-day EMA of the closing price
    k = ticker['Close'].ewm(span=12, adjust=False, min_periods=1).mean()
    # Get the 12-day EMA of the closing price
    d = ticker['Close'].ewm(span=26, adjust=False, min_periods=1).mean()
    # Subtract the 26-day EMA from the 12-Day EMA to get the MACD
    macd = k - d
    # Get the 9-Day EMA of the MACD for the Trigger line
    macd_s = macd.ewm(span=9, adjust=False, min_periods=1).mean()
    # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
    macd_h = macd - macd_s
    # Add all of our new values for the MACD to the dataframe
    ticker['macd'] = ticker.index.map(macd)
    ticker['macd_h'] = ticker.index.map(macd_h)
    ticker['macd_s'] = ticker.index.map(macd_s)
    return ticker

## function that calculates Average true range (ATR)
def ATR_calculation(ticker, n_s=[14,20,22]):
    for n in n_s:
        ticker[f'ATR_{n}'] = pd.Series(np.amax(np.vstack(((ticker['High'] - ticker['Low']), 
                                                          abs(ticker['High'] - ticker['Close']), 
                                                          abs(ticker['Low'] - ticker['Close']))).T, axis=1))
    return ticker

## function that calculates Relative strength index (RSI)
def RSI_calculation(ticker, period = 14):
    
    close_delta = ticker['Close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    ma_up = up.ewm(com = period - 1, adjust=True, min_periods = 1).mean()
    ma_down = down.ewm(com = period - 1, adjust=True, min_periods = 1).mean()

    rsi = ma_up / ma_down
    ticker['RSI'] = 100 - (100/(1 + rsi))
    return ticker

# Import macroeconomic data and preprocess

## function that converts monthly data to daily data through forward filling
def monthly_to_daily(df):
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d')
    df=df.set_index('DATE').resample('D').ffill()
    df = df.reset_index()
    df['DATE']=df['DATE'].dt.strftime('%Y-%m-%d')
    return df

# CBOE Volatility Index (Investor’s fear index)
VIX=pd.read_csv('/Users/joyceee_xby/Desktop/Project/macroeconomic_data/^VIX.csv')
VIX=VIX[['Date','Close']]
VIX=VIX.rename(columns={"Close": "VIX"})
# Interest Rate
DFF=pd.read_csv('/Users/joyceee_xby/Desktop/Project/macroeconomic_data/DFF.csv')
DFF.head()
# US dollar index
USDX=pd.read_csv('/Users/joyceee_xby/Desktop/Project/macroeconomic_data/DX-Y.NYB.csv')
USDX=USDX[['Date','Close']]
USDX=USDX.rename(columns={"Close": "USDX"})
# Civilian unemployment rate
UNRATE=pd.read_csv('/Users/joyceee_xby/Desktop/Project/macroeconomic_data/UNRATE.csv')
UNRATE=monthly_to_daily(UNRATE)
# Consumer sentiment index
UMCSENT=pd.read_csv('/Users/joyceee_xby/Desktop/Project/macroeconomic_data/UMCSENT.csv')
UMCSENT=monthly_to_daily(UMCSENT)

# Function that merges all data
def technical_macro_merge(ticker):
    ticker=MA_calculation(ticker,MAs = [5,10,20,50,100,200,500])
    ticker=MACD_calculation(ticker)
    ticker=ATR_calculation(ticker, n_s=[14,20,22])
    ticker=RSI_calculation(ticker,period=14)
    ticker=ticker.merge(VIX,how='left',on='Date')
    ticker=ticker.merge(DFF,how='left',left_on='Date',right_on='DATE')
    ticker=ticker.merge(USDX,how='left',on='Date')
    ticker=ticker.merge(UNRATE,how='left',left_on='Date',right_on='DATE')
    ticker=ticker.merge(UMCSENT,how='left',left_on='Date',right_on='DATE')
    ticker=ticker.drop(labels=['DATE_x','DATE_y','DATE'], axis=1)
    return ticker

# Generate holistic dataset for each ticker
for ticker in ticker_symbol_list:
    ticker_df=pd.read_csv('/Users/joyceee_xby/Desktop/Project/stock_data/'+ticker+'.csv')
    ticker_df=technical_macro_merge(ticker_df)
    ticker_df.to_csv('/Users/joyceee_xby/Desktop/Project/updated_data/'+ticker+'.csv')