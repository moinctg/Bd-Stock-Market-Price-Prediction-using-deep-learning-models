from django.shortcuts import render
from django.http import HttpResponse
from  urllib import request
from django.shortcuts import render 
from django.http import HttpResponse
from django.template import RequestContext

from plotly.offline import plot

import plotly.graph_objects as go

import plotly.express as px 

from plotly.graph_objs import Scatter 

import pandas as pd

import numpy as np 

import json 

import datetime as dt  
import yfinance as yf

from .models import Project

from sklearn.linear_model import LinearRegression 

from sklearn import preprocessing,model_selection,svm


# Create your views here.


def index(request):

    data = yf.download (
    #  passes the ticker 
    tickers=['AAPL','AMZN','QCOM','META','NVDA','JPM'],
    group_by = 'ticker',
    threads=True,

    period='imo',
    interval='id'
    )
    data.reset_index(level=0,inplace=True)

    fig_left= go.Figure()
    fig_left.add_trace(
        go.Scatter(x=data['Date'] , y=data['AAPL']['Adj Close'],name="AAPL")
    
    )
    fig_left.add_trace(
        go.Scatter(x=data['Date'], y=data['AMZN']['Adj Close'],name="AMZN")
    )
    fig_left.add_trace(
        go.Scatter(x=data['Date'], y=data['QCOM']['Adj Close'],name="QCOM")
    )
    fig_left.add_trace(
        go.Scatter(x=data['Date'], y=data['META']['Adj Close'],name="META")
    )
    fig_left.add_trace(
        go.Scatter(x=data['Date'], y=data['NVDA']['Adj Close'],name="NVDA")
    )
    fig_left.add_trace(
        go.Scatter(x=data['Date'], y=data['JPM']['Adj Close'],name="JPM")
    )
    fig_left.update_layout(paper_bgcolor="#14151b", plot_bgcolor="#14151b", font_color="white")
    plot_div_left = plot(fig_left,auto_open=False,output_type='div')


    df1 = yf.download(tickers='AAPL', period='1d' , interval='1d')
    df2 = yf.download(tickers='AMZN' ,period='id',interval='1d')
    df3 = yf.download(tickers = 'GOOGL', period='1d', interval='1d')
    df4 = yf.download(tickers = 'UBER', period='1d', interval='1d')
    df5 = yf.download(tickers = 'TSLA', period='1d', interval='1d')
    df6 = yf.download(tickers = 'TWTR', period='1d', interval='1d')

    df1.insert(0,'Ticker','AAPL')
    df2.insert(0,'Ticker','AMZN')
    df3.insert(0,'Ticker','GOOGL')
    df4.insert(0,'Ticker','UBER')
    df5.insert(0,'Ticker','TSLA')
    df6.insert(0,'Ticker','TWTR')

    df = pd.concat([df1,df2,df3,df4,df5,df6],axis=0)
    df.reset_index(level=0, inplace=True)
    df.columns = ['Date','Ticker','Open','High','Low','Close','Adj_Close','Volume']
    convert_dist = {'Date':object}
    df.drop("Date", axis=1, inplace=True)
    json_records = df.reset_index().to_json(orient='records')
    recent_stocks = []
    recent_stocks = json.loads(json_records)
   
    #    page render section 


    return render (request ,'index.html',{
        'plot_div_left': plot_div_left,
        'recent_stocks':recent_stocks
    })

def ticker (request):
    ticker_df = pd.read_csv('stockpredictionApp/Data/new_tickers.csv')
    json_ticker = ticker_df.reset_index().to_csv(orient='records')
    ticker_list = []
    ticker_list = json.loads(json_ticker)

    return render (request, 'ticker.html',{
        'ticker_list': ticker_list

    })


