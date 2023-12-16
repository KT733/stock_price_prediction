# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
from datetime import datetime
import visualization_functions

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

ticker_symbol_list=['TSLA', 'PLTR', 'UBER', 'MARA', 'NOK', 'NIO', 'AAL', 'F', 'PFE', 'LU', 'PLUG', 'RIOT', 'SOFI', 'NVDA', 'AMZN', 'INTC', 'BAC', 'AMD', 'T', 'CCL', 'BCS', 'AAPL', 'GOOGL', 'ERIC', 'RIVN', 'GM', 'VALE', 'PATH', 'MSFT', 'AFRM', 'GRAB', 'KGC', 'NU', 'NCLH', 'DNA', 'CMCSA', 'VZ', 'CVNA', 'XOM', 'KEY', 'ALK', 'SNAP', 'BABA', 'COIN', 'GOOG', 'WBD', 'GME', 'C', 'OPEN', 'GOLD', 'LCID', 'BBD', 'LYFT', 'CSCO', 'HOOD', 'PBR', 'HEP', 'HBAN', 'KVUE', 'META', 'DKNG', 'CSX', 'PCG', 'MPW', 'CNHI', 'RUN', 'M', 'UPST', 'FHN', 'RIG', 'NEM', 'IMGN', 'AGNC', 'HPE', 'PINS', 'PYPL', 'PARA', 'WFC', 'RLX', 'MRVL', 'GGB', 'SIRI', 'BTG', 'CPNG', 'LUV', 'PTON', 'CHWY', 'FCX', 'CVX', 'SWN', 'KMI', 'U', 'VTRS', 'SCHW', 'KO', 'LYG', 'AMCR', 'TSM', 'XPEV', 'QS', 'OXY', 'ENB', 'BMY', 'NEE', 'CRM', 'NKE', 'USB', 'S', 'DAL', 'PBR-A', 'AI', 'WBA', 'IBN', 'DIS', 'IONQ', 'VFC', 'SBUX', 'BSX', 'ABEV', 'TAL', 'SE', 'BTE', 'SHOP', 'JD', 'CFLT', 'BP', 'PDD', 'EQH', 'CLF', 'UEC', 'TFC', 'JNJ', 'MTCH', 'GPS', 'ET', 'EVRG', 'AVTR', 'MRO', 'SQ', 'RF', 'ITUB', 'WMT', 'JWN', 'VRT', 'KHC', 'SNOW', 'MU', 'ZM', 'RBLX', 'CVE', 'IOT', 'DISH', 'TGT', 'OWL', 'AES', 'CRBG', 'JPM', 'BBWI', 'HUT', 'CVS', 'TEVA', 'CLVT', 'SBSW', 'YMM', 'ELAN', 'HL', 'IQ', 'KSS', 'UAL', 'TTD', 'IVZ', 'EL', 'MRK', 'TOST', 'EQT', 'TME', 'FIVN', 'DVN', 'DELL', 'MS', 'SPOT', 'NYCB', 'STLA', 'UMC', 'CNP', 'MO', 'HMY', 'NI', 'EXC', 'SLB', 'VFS', 'MDT', 'BZ', 'O', 'ABR', 'VICI', 'HAL', 'VOD', 'PEAK', 'DOW', 'FIS', 'GTLB', 'SHEL', 'AUR', 'PR', 'CTRA', 'TJX', 'ARRY', 'IBM', 'FOXA', 'VST', 'PTEN', 'PM', 'QCOM', 'LI', 'ZI', 'NLY', 'INFY', 'ALKS', 'LTHM', 'RTX', 'D', 'ON', 'BEKE', 'STNE', 'ORCL', 'GNW', 'BILI', 'PLD', 'X', 'KDP', 'CFG', 'GILD', 'PSTG', 'PEP', 'ABNB', 'ROKU', 'V', 'BXSL', 'WMB', 'FITB', 'BA', 'JOBY', 'COTY', 'WOLF', 'KR', 'TLKMF', 'GFI', 'NXE', 'ARM']

app.layout = html.Div(children=[
    html.H1(children='Stock Price Graphs & Predictions', style={'textAlign': 'left'}),

    html.Div(children='''
        You can check out the historical prices, volume, and related technical indicators of the most active list of stocks by choosing from the dropdown bar below!
    '''),
    
    html.Label('Ticker Symbols'),
    dcc.Dropdown(ticker_symbol_list,'AMZN',id='ticker'),
    
    html.Label('Chart Types'),
    html.Div([
            dcc.RadioItems(
                ['Time Series Chart','Candlestick Chart', 'OHLC Chart'],
                'Time Series Chart',
                id='chart',
                inline=False
            )
        ], style={'width': '50%'}),
    
    html.Label('Indices'),
    html.Div([
    dcc.Checklist(['Moving Average (MA)','Moving Average Convergence Divergence (MACD)',
                   'Average True Rate (ATR)','Relative Strength Index (RSI)'],
                  id='indice',
                  inline=False)],
        style={'width': '50%'}),
    dcc.Graph(id='price_graph', figure={})
], style={'padding': 10, 'flex': 1})

@callback(
    Output('price_graph', 'figure'),
    Input('ticker', 'value'),
    Input('chart', 'value'),
    Input('indice', 'value')
)
def update_graph(ticker,chart,indice):
    df=pd.read_csv('/Users/joyceee_xby/Desktop/Project/updated_data/'+ticker+'.csv')
    
    # default graph
    price_graph=visualization_functions.default_graph(df,ticker,chart)
    # update title
    price_graph=visualization_functions.update_title(price_graph,ticker,chart)
    # graph with indice choices
    for choice in visualization_functions.all_choices:
        if indice==choice:
            if len(choice)==1:
                price_graph=visualization_functions.one_indice(df,ticker,chart,choice)
            elif len(choice)==2:
                price_graph=visualization_functions.two_indices(df,ticker,chart,choice)
            elif len(choice)==3:
                price_graph=visualization_functions.three_indices(df,ticker,chart,choice)
            elif len(choice)==4:
                price_graph=visualization_functions.four_indices(df,ticker,chart,choice)
        price_graph=visualization_functions.update_title(price_graph,ticker,chart)
    return price_graph

if __name__ == '__main__':
    app.run(debug=True)
