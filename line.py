from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go
import pandas as pd
from numpy import arange,array,ones
import os.path
import time
from scipy import stats

start_time = time.time()


def getOptions():
    options = []

    df = pd.read_csv('data/GlobalLandTemperaturesByCountry.csv')
    countries = list(df['Country'].unique())
    countries.append('Global')

    for country in countries:
        option = {'label': country, 'value': country}
        options.append(option)

    return options

def getDataByDateRange(df, country, start = 1750, end = 2015):
    # Create a trace
    data = []

    if country != 'Global':
        y = df[(df['Country'] == country) & (df['dt'] > start) & (df['dt'] <= end)]['AverageTemperature']
        x = df[(df['Country'] == country) & (df['dt'] > start) & (df['dt'] <= end)]['dt']
        xi = arange(0, len(x))
    else:
        print(list(df))
        y = df['LandAverageTemperature']
        x = df['dt']
        xi = arange(0, len(x))
        
    # Generated linear fit
    slope, intercept, _, _, _ = stats.linregress(xi, y)

    line = slope*xi+intercept

    trace1 = go.Scatter(
                      x=x,
                      y=y,
                      mode='markers',
                      marker=go.Marker(color='rgb(255, 127, 14)'),
                      name='Data'
                      )

    trace2 = go.Scatter(
                      x=x,
                      y=line,
                      mode='lines',
                      marker=go.Marker(color='rgb(31, 119, 180)'),
                      name='Fit'
                      )

    data.append(trace1)
    data.append(trace2)

    return data

def getFigure(data, country = 'Netherlands', start = 1750, end = 2015):
    data = getDataByDateRange(data, country, start, end)
    layout = dict(title = country + ' Average Temperature between ' + str(start) + ' - ' + str(end),
                  xaxis = dict(title = 'Year -->'),
                  yaxis = dict(title = 'Temperature in °C -->'),
                )

    return dict(data = data, layout = layout)

def createScatter(data, country = 'Netherlands', start = 1750, end = 2015):
    print("--- %s seconds --- Started creating GDP- and Temperaturegrowth by year " % (time.time() - start_time))

    fig = getFigure(data, country)
    plot(fig, filename='climate_change_scatter-and-line.html' )

def getGlobalData():
    if os.path.isfile('data/df_global2.csv'):
        df = pd.read_csv('data/df_global.csv')
    else:
        df = pd.read_csv('data/GlobalTemperatures.csv')
        df = df.dropna()
        df['dt'] = pd.to_datetime(df['dt'], format='%Y-%m-%d')

        df = df.groupby([pd.Grouper(key='dt', freq='1Y')]).mean().reset_index()

        years = list(range(1750, 2014))
        df = df[pd.DatetimeIndex(df['dt']).year.isin(years)]

        # Remove month and day from full date 
        df['dt'] = pd.DatetimeIndex(df['dt']).year
        df.to_csv('data/df_global.csv')
    return df

def getData():
    if os.path.isfile('data/df_r.csv'):
        df = pd.read_csv('data/df_gdp.csv')
        df['dt'] = pd.to_datetime(df['dt'], format='%Y-%m-%d')
    else:
        # Reading the dataset and storing it
        df = pd.read_csv('data/GlobalLandTemperaturesByCountry.csv')

        # Remove all empty elements
        df = df.dropna()

        # Cast string to datetime
        df['dt'] = pd.to_datetime(df['dt'], format='%Y-%m-%d')

        # Merge all monthly items to one year item
        df = df.groupby([pd.Grouper(key='dt', freq='1Y'), 'Country']).mean().reset_index()

        # Remove all dates not in scope
        years = list(range(1750, 2014))
        df = df[pd.DatetimeIndex(df['dt']).year.isin(years)]
        # Remove month and day from full date 
        df['dt'] = pd.DatetimeIndex(df['dt']).year
        df.to_csv('data/df_gdp.csv')

    return df

if __name__ == '__main__':
    country = 'Global'
    start = 1900
    end = 2015

    if country != 'Global':
        df = getData()
    else:
        df = getGlobalData()


    createScatter(data, country, start=start, end=end)
