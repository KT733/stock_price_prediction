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
from itertools import permutations
from itertools import combinations

indices=['Moving Average (MA)','Moving Average Convergence Divergence (MACD)',
                   'Average True Rate (ATR)','Relative Strength Index (RSI)']

one_choice=[['Moving Average (MA)'],['Moving Average Convergence Divergence (MACD)'],
                ['Average True Rate (ATR)'],['Relative Strength Index (RSI)']]

def permutation_to_list(comb):
    new_list=[]
    for i in list(comb):
        i=list(i)
        new_list.append(i)
    return new_list

all_choices=[]
for i in range(1,5):
    perm=permutations(indices,i)
    perm=permutation_to_list(perm)
    all_choices=all_choices+perm

def default_graph(df,ticker,chart):
    price_graph = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.05, subplot_titles=('Price', 'Volume'),row_width=[0.3,0.7])
    if chart=='Time Series Chart':
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df["Close"],mode='lines',showlegend=True,name="Close"),row=1,col=1)
    elif chart=='Candlestick Chart':
        price_graph.add_trace(go.Candlestick(x=df['Date'],open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'],
                                             showlegend=True,name="Candlestick"),row=1,col=1)
    elif chart=='OHLC Chart':
        price_graph.add_trace(go.Ohlc(x=df['Date'],open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'],
                                      showlegend=True,name="OHLC"),row=1,col=1)
    price_graph.add_trace(go.Bar(x=df['Date'], y=df['Volume'],showlegend=True,name="Volume",marker=dict(color='red')), row=2, col=1)
    price_graph.update_layout(legend_orientation="v", xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=True, xaxis2_rangeslider_thickness=0.05)
    price_graph.update_layout(height=700, width=1350)
    return price_graph

def price_volume_graph_by_chart(price_graph,df,chart):
    if chart=='Time Series Chart':
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df["Close"],mode='lines',showlegend=True,name="Close"),row=1,col=1)
    elif chart=='Candlestick Chart':
        price_graph.add_trace(go.Candlestick(x=df['Date'],open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'],
                                             showlegend=True,name="Candlestick"),row=1,col=1)
    elif chart=='OHLC Chart':
        price_graph.add_trace(go.Ohlc(x=df['Date'],open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'],
                                      showlegend=True,name="OHLC"),row=1,col=1)
    price_graph.add_trace(go.Bar(x=df['Date'], y=df['Volume'],showlegend=True,name='Volume'), row=2, col=1)
    return price_graph

def update_title(price_graph,ticker,chart):
    if chart=='Time Series Chart':
        price_graph.update_layout(title_text=ticker+" Stock Price & Volume Time Series Chart")
    elif chart=='Candlestick Chart':
        price_graph.update_layout(title_text=ticker+" Stock Price & Volume Candlestick Chart")
    elif chart=='OHLC Chart':
        price_graph.update_layout(title_text=ticker+" Stock Price & Volume OHLC Chart")
    return price_graph

def one_indice(df,ticker,chart,choice):
    rows = len(df.axes[0])
    if choice==['Moving Average (MA)']:
        price_graph = default_graph(df,ticker,chart)
        for ma in [5,10,20,50,100,200,500]:
            price_graph.add_trace(go.Scatter(x=df['Date'], y=df[f'MA_{ma}'],mode='lines',
                                             showlegend=True,name=f'MA{ma}'),row=1,col=1)
    elif choice==['Moving Average Convergence Divergence (MACD)']:
        price_graph = make_subplots(rows=3, cols=1, shared_xaxes=True, 
           vertical_spacing=0.05, subplot_titles=('Price', 'Volume','Moving Average Convergence Divergence'),row_width=[0.3,0.3,0.7])
        price_graph = price_volume_graph_by_chart(price_graph,df,chart)
        price_graph.add_trace(go.Bar(x=df['Date'], y=df['macd_h'],showlegend=True,name='MACD Histogram',
                                    marker=dict(color=['red' if df.iloc[row,16]<0 else 'green' for row in range(rows)])), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd'],showlegend=True,name='MACD',mode='lines',
                                    marker=dict(color='blue')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd_s'],showlegend=True,name='MACD Signal',mode='lines',
                                    marker=dict(color='yellow')), row=3, col=1)
        price_graph.update_layout(legend_orientation="v", xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=False,
         xaxis3_rangeslider_visible=True, xaxis3_rangeslider_thickness=0.05)
        price_graph.update_layout(height=900, width=1350)
    elif choice==['Average True Rate (ATR)']:
        price_graph = make_subplots(rows=3, cols=1, shared_xaxes=True, 
           vertical_spacing=0.05, subplot_titles=('Price', 'Volume','Average True Range'),row_width=[0.3,0.3,0.7])
        price_graph = price_volume_graph_by_chart(price_graph,df,chart)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['ATR_14'],showlegend=True,name='ATR14',mode='lines',
                                    marker=dict(color='purple')), row=3, col=1)
        price_graph.update_layout(legend_orientation="v",xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=False,
         xaxis3_rangeslider_visible=True, xaxis3_rangeslider_thickness=0.05)
        price_graph.update_layout(height=900, width=1350)
    elif choice==['Relative Strength Index (RSI)']:
        price_graph = make_subplots(rows=3, cols=1, shared_xaxes=True, 
           vertical_spacing=0.05, subplot_titles=('Price', 'Volume','Relative Strength Index'),row_width=[0.3,0.3,0.7])
        price_graph = price_volume_graph_by_chart(price_graph,df,chart)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['RSI'],showlegend=True,name='RSI',mode='lines',
                                    marker=dict(color='brown')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 70),showlegend=True,name='Overbought',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='green')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 30),showlegend=True,name='Oversold',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='red')), row=3, col=1)
        price_graph.update_layout(legend_orientation="v", xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=False,
         xaxis3_rangeslider_visible=True, xaxis3_rangeslider_thickness=0.05)
        price_graph.update_layout(height=900, width=1350)
    return price_graph

def two_indices(df,ticker,chart,choice):
    rows = len(df.axes[0])
    if choice in permutation_to_list(permutations(['Moving Average (MA)','Moving Average Convergence Divergence (MACD)'], 2)):
        price_graph = make_subplots(rows=3, cols=1, shared_xaxes=True, 
           vertical_spacing=0.05, subplot_titles=('Price', 'Volume','Moving Average Convergence Divergence'),row_width=[0.3,0.3,0.7])
        price_graph = price_volume_graph_by_chart(price_graph,df,chart)
        for ma in [5,10,20,50,100,200,500]:
            price_graph.add_trace(go.Scatter(x=df['Date'], y=df[f'MA_{ma}'],mode='lines',
                                             showlegend=True,name=f'MA{ma}'),row=1,col=1)
        price_graph.add_trace(go.Bar(x=df['Date'], y=df['macd_h'],showlegend=True,name='MACD Histogram',
                                    marker=dict(color=['red' if df.iloc[row,16]<0 else 'green' for row in range(rows)])), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd'],showlegend=True,name='MACD',mode='lines',
                                    marker=dict(color='blue')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd_s'],showlegend=True,name='MACD Signal',mode='lines',
                                    marker=dict(color='yellow')), row=3, col=1)
        price_graph.update_layout(legend_orientation="v", xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=False,
         xaxis3_rangeslider_visible=True, xaxis3_rangeslider_thickness=0.05)
        price_graph.update_layout(height=900, width=1350)
    elif choice in permutation_to_list(permutations(['Moving Average (MA)', 'Average True Rate (ATR)'], 2)):
        price_graph = make_subplots(rows=3, cols=1, shared_xaxes=True, 
           vertical_spacing=0.05, subplot_titles=('Price', 'Volume','Average True Rate'),row_width=[0.3,0.3,0.7])
        price_graph = price_volume_graph_by_chart(price_graph,df,chart)
        for ma in [5,10,20,50,100,200,500]:
            price_graph.add_trace(go.Scatter(x=df['Date'], y=df[f'MA_{ma}'],mode='lines',
                                             showlegend=True,name=f'MA{ma}'),row=1,col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['ATR_14'],showlegend=True,name='ATR14',mode='lines',
                                    marker=dict(color='purple')), row=3, col=1)
        price_graph.update_layout(legend_orientation="v", xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=False,
         xaxis3_rangeslider_visible=True, xaxis3_rangeslider_thickness=0.05)
        price_graph.update_layout(height=900, width=1350)
    elif choice in permutation_to_list(permutations(['Moving Average (MA)', 'Relative Strength Index (RSI)'], 2)):
        price_graph = make_subplots(rows=3, cols=1, shared_xaxes=True, 
           vertical_spacing=0.05, subplot_titles=('Price', 'Volume','Relative Strength Index'),row_width=[0.3,0.3,0.7])
        price_graph = price_volume_graph_by_chart(price_graph,df,chart)
        for ma in [5,10,20,50,100,200,500]:
            price_graph.add_trace(go.Scatter(x=df['Date'], y=df[f'MA_{ma}'],mode='lines',
                                             showlegend=True,name=f'MA{ma}'),row=1,col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['RSI'],showlegend=True,name='RSI',mode='lines',
                                    marker=dict(color='brown')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 70),showlegend=True,name='Overbought',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='green')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 30),showlegend=True,name='Oversold',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='red')), row=3, col=1)
        price_graph.update_layout(legend_orientation="v",xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=False,
         xaxis3_rangeslider_visible=True, xaxis3_rangeslider_thickness=0.05)
        price_graph.update_layout(height=900, width=1350)
    elif choice in permutation_to_list(permutations(['Moving Average Convergence Divergence (MACD)', 'Average True Rate (ATR)'], 2)):
        price_graph = make_subplots(rows=4, cols=1, shared_xaxes=True, 
           vertical_spacing=0.05, subplot_titles=('Price', 'Volume','Moving Average Convergence Divergence','Average True Rate',),row_width=[0.3,0.3,0.3,0.7])
        price_graph = price_volume_graph_by_chart(price_graph,df,chart)
        price_graph.add_trace(go.Bar(x=df['Date'], y=df['macd_h'],showlegend=True,name='MACD Histogram',
                                    marker=dict(color=['red' if df.iloc[row,16]<0 else 'green' for row in range(rows)])), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd'],showlegend=True,name='MACD',mode='lines',
                                    marker=dict(color='blue')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd_s'],showlegend=True,name='MACD Signal',mode='lines',
                                    marker=dict(color='yellow')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['ATR_14'],showlegend=True,name='ATR14',mode='lines',
                                    marker=dict(color='purple')), row=4, col=1)
        price_graph.update_layout(legend_orientation="v", xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=False,
         xaxis3_rangeslider_visible=False, xaxis4_rangeslider_visible=True,xaxis4_rangeslider_thickness=0.05)
        price_graph.update_layout(height=1100, width=1350)
    elif choice in permutation_to_list(permutations(['Moving Average Convergence Divergence (MACD)', 'Relative Strength Index (RSI)'], 2)):
        price_graph = make_subplots(rows=4, cols=1, shared_xaxes=True, 
           vertical_spacing=0.05, subplot_titles=('Price', 'Volume','Moving Average Convergence Divergence','Relative Strength Index',),row_width=[0.3,0.3,0.3,0.7])
        price_graph = price_volume_graph_by_chart(price_graph,df,chart)
        price_graph.add_trace(go.Bar(x=df['Date'], y=df['macd_h'],showlegend=True,name='MACD Histogram',
                                    marker=dict(color=['red' if df.iloc[row,16]<0 else 'green' for row in range(rows)])), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd'],showlegend=True,name='MACD',mode='lines',
                                    marker=dict(color='blue')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd_s'],showlegend=True,name='MACD Signal',mode='lines',
                                    marker=dict(color='yellow')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['RSI'],showlegend=True,name='RSI',mode='lines',
                                    marker=dict(color='brown')), row=4, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 70),showlegend=True,name='Overbought',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='green')), row=4, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 30),showlegend=True,name='Oversold',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='red')), row=4, col=1)
        price_graph.update_layout(legend_orientation="v", xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=False,
         xaxis3_rangeslider_visible=False, xaxis4_rangeslider_visible=True,xaxis4_rangeslider_thickness=0.05)
        price_graph.update_layout(height=1100, width=1350)
    elif choice in permutation_to_list(permutations(['Average True Rate (ATR)', 'Relative Strength Index (RSI)'], 2)):
        price_graph = make_subplots(rows=4, cols=1, shared_xaxes=True, 
           vertical_spacing=0.05, subplot_titles=('Price', 'Volume','Average True Rate','Relative Strength Index'),row_width=[0.3,0.3,0.3,0.7])
        price_graph = price_volume_graph_by_chart(price_graph,df,chart)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['ATR_14'],showlegend=True,name='ATR14',mode='lines',
                                    marker=dict(color='purple')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['RSI'],showlegend=True,name='RSI',mode='lines',
                                    marker=dict(color='brown')), row=4, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 70),showlegend=True,name='Overbought',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='green')), row=4, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 30),showlegend=True,name='Oversold',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='red')), row=4, col=1)
        price_graph.update_layout(legend_orientation="v", xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=False,
         xaxis3_rangeslider_visible=False, xaxis4_rangeslider_visible=True,xaxis4_rangeslider_thickness=0.05)
        price_graph.update_layout(height=1100, width=1350)
    return price_graph

def three_indices(df,ticker,chart,choice):
    rows = len(df.axes[0])
    if choice in permutation_to_list(permutations(['Moving Average (MA)','Moving Average Convergence Divergence (MACD)','Average True Rate (ATR)'], 3)):
        price_graph = make_subplots(rows=4, cols=1, shared_xaxes=True, 
           vertical_spacing=0.05, subplot_titles=('Price', 'Volume','Moving Average Convergence Divergence','Average True Rate'),row_width=[0.3,0.3,0.3,0.7])
        price_graph = price_volume_graph_by_chart(price_graph,df,chart)
        for ma in [5,10,20,50,100,200,500]:
            price_graph.add_trace(go.Scatter(x=df['Date'], y=df[f'MA_{ma}'],mode='lines',
                                             showlegend=True,name=f'MA{ma}'),row=1,col=1)
        price_graph.add_trace(go.Bar(x=df['Date'], y=df['macd_h'],showlegend=True,name='MACD Histogram',
                                    marker=dict(color=['red' if df.iloc[row,16]<0 else 'green' for row in range(rows)])), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd'],showlegend=True,name='MACD',mode='lines',
                                    marker=dict(color='blue')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd_s'],showlegend=True,name='MACD Signal',mode='lines',
                                    marker=dict(color='yellow')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['ATR_14'],showlegend=True,name='ATR14',mode='lines',
                                    marker=dict(color='purple')), row=4, col=1)
        price_graph.update_layout(legend_orientation="v", xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=False,
         xaxis3_rangeslider_visible=False, xaxis4_rangeslider_visible=True,xaxis4_rangeslider_thickness=0.05)
        price_graph.update_layout(height=1100, width=1350)
    elif choice in permutation_to_list(permutations(['Moving Average (MA)','Moving Average Convergence Divergence (MACD)','Relative Strength Index (RSI)'], 3)):
        price_graph = make_subplots(rows=4, cols=1, shared_xaxes=True, 
           vertical_spacing=0.05, subplot_titles=('Price', 'Volume','Moving Average Convergence Divergence','Relative Strength Index'),row_width=[0.3,0.3,0.3,0.7])
        price_graph = price_volume_graph_by_chart(price_graph,df,chart)
        for ma in [5,10,20,50,100,200,500]:
            price_graph.add_trace(go.Scatter(x=df['Date'], y=df[f'MA_{ma}'],mode='lines',
                                             showlegend=True,name=f'MA{ma}'),row=1,col=1)
        price_graph.add_trace(go.Bar(x=df['Date'], y=df['macd_h'],showlegend=True,name='MACD Histogram',
                                    marker=dict(color=['red' if df.iloc[row,16]<0 else 'green' for row in range(rows)])), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd'],showlegend=True,name='MACD',mode='lines',
                                    marker=dict(color='blue')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd_s'],showlegend=True,name='MACD Signal',mode='lines',
                                    marker=dict(color='yellow')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['RSI'],showlegend=True,name='RSI',mode='lines',
                                    marker=dict(color='brown')), row=4, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 70),showlegend=True,name='Overbought',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='green')), row=4, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 30),showlegend=True,name='Oversold',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='red')), row=4, col=1)
        price_graph.update_layout(legend_orientation="v", xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=False,
         xaxis3_rangeslider_visible=False, xaxis4_rangeslider_visible=True,xaxis4_rangeslider_thickness=0.05)
        price_graph.update_layout(height=1100, width=1350)
    elif choice in permutation_to_list(permutations(['Moving Average (MA)','Average True Rate (ATR)','Relative Strength Index (RSI)'], 3)):
        price_graph = make_subplots(rows=4, cols=1, shared_xaxes=True, 
           vertical_spacing=0.05, subplot_titles=('Price', 'Volume','Average True Rate','Relative Strength Index'),row_width=[0.3,0.3,0.3,0.7])
        price_graph = price_volume_graph_by_chart(price_graph,df,chart)
        for ma in [5,10,20,50,100,200,500]:
            price_graph.add_trace(go.Scatter(x=df['Date'], y=df[f'MA_{ma}'],mode='lines',
                                             showlegend=True,name=f'MA{ma}'),row=1,col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['ATR_14'],showlegend=True,name='ATR14',mode='lines',
                                    marker=dict(color='purple')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['RSI'],showlegend=True,name='RSI',mode='lines',
                                    marker=dict(color='brown')), row=4, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 70),showlegend=True,name='Overbought',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='green')), row=4, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 30),showlegend=True,name='Oversold',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='red')), row=4, col=1)
        price_graph.update_layout(legend_orientation="v", xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=False,
         xaxis3_rangeslider_visible=False, xaxis4_rangeslider_visible=True,xaxis4_rangeslider_thickness=0.05)
        price_graph.update_layout(height=1100, width=1350)
    elif choice in permutation_to_list(permutations(['Moving Average Convergence Divergence (MACD)','Average True Rate (ATR)','Relative Strength Index (RSI)'], 3)):
        price_graph = make_subplots(rows=5, cols=1, shared_xaxes=True, 
           vertical_spacing=0.05, subplot_titles=('Price', 'Volume','Moving Average Convergence Divergence','Average True Rate','Relative Strength Index'),row_width=[0.3,0.3,0.3,0.3,0.7])
        price_graph = price_volume_graph_by_chart(price_graph,df,chart)
        price_graph.add_trace(go.Bar(x=df['Date'], y=df['macd_h'],showlegend=True,name='MACD Histogram',
                                    marker=dict(color=['red' if df.iloc[row,16]<0 else 'green' for row in range(rows)])), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd'],showlegend=True,name='MACD',mode='lines',
                                    marker=dict(color='blue')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd_s'],showlegend=True,name='MACD Signal',mode='lines',
                                    marker=dict(color='yellow')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['ATR_14'],showlegend=True,name='ATR14',mode='lines',
                                    marker=dict(color='purple')), row=4, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['RSI'],showlegend=True,name='RSI',mode='lines',
                                    marker=dict(color='brown')), row=5, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 70),showlegend=True,name='Overbought',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='green')), row=5, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 30),showlegend=True,name='Oversold',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='red')), row=5, col=1)
        price_graph.update_layout(legend_orientation="v", xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=False,
         xaxis3_rangeslider_visible=False, xaxis4_rangeslider_visible=False, xaxis5_rangeslider_visible=True,xaxis5_rangeslider_thickness=0.05)
        price_graph.update_layout(height=1300, width=1350)
    return price_graph

def four_indices(df,ticker,chart,choice):
    rows = len(df.axes[0])
    if choice in permutation_to_list(permutations(indices, 4)):
        price_graph = make_subplots(rows=5, cols=1, shared_xaxes=True, 
           vertical_spacing=0.05, subplot_titles=('Price', 'Volume','Moving Average Convergence Divergence','Average True Rate','Relative Strength Index'),row_width=[0.3,0.3,0.3,0.3,0.7])
        price_graph = price_volume_graph_by_chart(price_graph,df,chart)
        for ma in [5,10,20,50,100,200,500]:
            price_graph.add_trace(go.Scatter(x=df['Date'], y=df[f'MA_{ma}'],mode='lines',
                                             showlegend=True,name=f'MA{ma}'),row=1,col=1)
        price_graph.add_trace(go.Bar(x=df['Date'], y=df['macd_h'],showlegend=True,name='MACD Histogram',
                                    marker=dict(color=['red' if df.iloc[row,16]<0 else 'green' for row in range(rows)])), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd'],showlegend=True,name='MACD',mode='lines',
                                    marker=dict(color='blue')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['macd_s'],showlegend=True,name='MACD Signal',mode='lines',
                                    marker=dict(color='yellow')), row=3, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['ATR_14'],showlegend=True,name='ATR14',mode='lines',
                                    marker=dict(color='purple')), row=4, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=df['RSI'],showlegend=True,name='RSI',mode='lines',
                                    marker=dict(color='brown')), row=5, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 70),showlegend=True,name='Overbought',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='green')), row=5, col=1)
        price_graph.add_trace(go.Scatter(x=df['Date'], y=np.full(rows, 30),showlegend=True,name='Oversold',mode='lines',
                                    line = dict(dash='dash'),marker=dict(color='red')), row=5, col=1)
        price_graph.update_layout(legend_orientation="v", xaxis1_rangeslider_visible=False,xaxis2_rangeslider_visible=False,
         xaxis3_rangeslider_visible=False, xaxis4_rangeslider_visible=False, xaxis5_rangeslider_visible=True,xaxis5_rangeslider_thickness=0.05)
        price_graph.update_layout(height=1300, width=1350)
    return price_graph