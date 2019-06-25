#!/usr/bin/env python
# coding: utf-8

# In[11]:


import requests
import pandas as pd
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource, ColumnDataSource, DatetimeTickFormatter, Range1d, HoverTool, CrosshairTool
from bokeh.embed import components
from flask import Flask, render_template, request, redirect


# In[12]:


app = Flask(__name__)


# In[13]:


def req_data(ticker):
    url="https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker="+ticker+"&qopts.columns=date,close&api_key=LG2WsxMs_SwDXxbBfxGc"
    page = requests.get(url)
    json = page.json()
    df = pd.DataFrame(json['datatable']['data'], columns=['date','close'])
    df['date'] = pd.to_datetime(df['date'])
    df['date_str'] = df['date'].map(lambda x: x.strftime("%Y-%m-%d"))
    df['close_str'] = df['close'].map(lambda x: '{:,.2f}'.format(x))
    return df


# In[14]:


def plot_bokeh(df, ticker):
    p = figure(width=800, height=400, title=ticker.upper(), tools="")

    hover = HoverTool(tooltips = """
    <div>
    <table>
    <tr><td class="ttlab">Date:</td><td>@date_str</td></tr>
    <tr><td class="ttlab">Close:</td><td>@close_str</td></tr>
    </table>
    </div>
    """)

    hover.mode = 'vline'
    hover.line_policy = 'nearest'
    p.add_tools(hover)

    crosshair = CrosshairTool()
    crosshair.dimensions = 'height'
    crosshair.line_color = "#ffffff"
    p.add_tools(crosshair)

    dfcds = ColumnDataSource(df)
    p.line('date', 'close', source = dfcds, color="#44ddaa")

    p.xaxis.formatter=DatetimeTickFormatter(days=["%d %b"])
    p.x_range=Range1d(df['date'].min(), df['date'].max())

    p.toolbar.logo = None
    p.toolbar_location = None

    return p


# In[15]:


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')


# In[16]:


@app.route('/graph', methods=['POST'])
def graph():
    tick = request.form['ticker_input'].upper()
    ticker_df = req_data(tick)
    graph = plot_bokeh(ticker_df, tick)
    script, div = components(graph)
    
    return render_template('graph.html', div = div, script = script)


# In[ ]:


if __name__ == '__main__':
    app.run()


# In[ ]:




