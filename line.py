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

def getDataByCountryByDateRange(df, country, start = 1750, end = 2015):
    y_min = df[(df['Country'] == country) & (df['dt'] > start) & (df['dt'] <= end)]['Min']
    y_avg = df[(df['Country'] == country) & (df['dt'] > start) & (df['dt'] <= end)]['AverageTemperature']
    y_max = df[(df['Country'] == country) & (df['dt'] > start) & (df['dt'] <= end)]['Max']
    x = df[(df['Country'] == country) & (df['dt'] > start) & (df['dt'] <= end)]['dt']
    xi = arange(0, len(x))

    # Generated linear fit for minumum temperature
    min_slope, min_intercept, _, _, _ = stats.linregress(xi, y_min)

    min_line = min_slope*xi+min_intercept

    # Generated linear fit for minumum temperature
    avg_slope, avg_intercept, _, _, _ = stats.linregress(xi, y_avg)

    avg_line = avg_slope*xi+avg_intercept

    # Generated linear fit for minumum temperature
    max_slope, max_intercept, _, _, _ = stats.linregress(xi, y_max)

    max_line = max_slope*xi+max_intercept

    traceMin = go.Scatter(
                      x=x,
                      y=y_min,
                      mode='markers',
                      marker=go.Marker(color='rgb(153, 153, 255)'),
                      name='Min'
                      )

    lineMin = go.Scatter(
                      x=x,
                      y=min_line,
                      mode='lines',
                      marker=go.Marker(color='rgb(0, 0, 255)'),
                      name='Min Fit'
                      )

    traceAvg = go.Scatter(
                      x=x,
                      y=y_avg,
                      mode='markers',
                      marker=go.Marker(color='rgb(255, 204, 153)'),
                      name='Average'
                      )

    lineAvg = go.Scatter(
                      x=x,
                      y=avg_line,
                      mode='lines',
                      marker=go.Marker(color='rgb(255, 153, 51)'),
                      name='Average Fit'
                      )

    traceMax = go.Scatter(
                      x=x,
                      y=y_max,
                      mode='markers',
                      marker=go.Marker(color='rgb(255, 153, 153)'),
                      name='Max'
                      )
    lineMax = go.Scatter(
                      x=x,
                      y=max_line,
                      mode='marker',
                      marker=go.Marker(color='rgb(255, 0, 0)'),
                      name='Max Fit'
                      )

    return [traceMin, lineMin, traceAvg, lineAvg, traceMax, lineMax]

def getGlobalDataByDateRange(df, country, start = 1750, end = 2015):

    maxAllowed = df[df['dt'] == 1850]['LandAverageTemperature'] + 2

    y = df[(df['dt'] > start) & (df['dt'] <= end)]['LandAverageTemperature']
    x = df[(df['dt'] > start) & (df['dt'] <= end)]['dt']

    xi = arange(0, len(x))
        
    # Generated linear fit
    slope, intercept, _, _, _ = stats.linregress(xi, y)

    line = slope*xi+intercept

    trace1 = go.Scatter(
                      x=x,
                      y=y,
                      mode='markers',
                      marker=go.Marker(color='rgb(255, 204, 153)'),
                      name='Temperature scatter'
                      )

    trace2 = go.Scatter(
                      x=x,
                      y=line,
                      mode='lines',
                      marker=go.Marker(color='rgb(255, 153, 51)'),
                      name='Fitted line'
                      )

    traceMax = go.Scatter(
                      x=x,
                      y=[maxAllowed[0]] * len(x),
                      line = dict(
                        color = ('rgb(205, 12, 24)'),
                        width = 2,
                        dash = 'dot'),
                    name='Maximum allowed temperature'
                      )


    return [trace1, trace2, traceMax]

def getFigure(df, country = 'Netherlands', start = 1750, end = 2015):
    print("--- %s seconds --- Getting figure of scatterplot with fitted line" % (time.time() - start_time))

    if (country == 'Global'):
        data = getGlobalDataByDateRange(df, country, start, end)
    else:
        data = getDataByCountryByDateRange(df, country, start, end)
    layout = dict(title = country + ' - maximum, average and minimum temperature between ' + str(start) + ' - ' + str(end),
                  xaxis = dict(title = 'Year -->'),
                  yaxis = dict(title = 'Temperature in °C -->'),
                )

    return dict(data = data, layout = layout)

def createScatter(df, country = 'Netherlands', start = 1750, end = 2015):
    print("--- %s seconds --- Plotting figure of scatterplot with fitted line" % (time.time() - start_time))
    fig = getFigure(df, country, start, end)
    plot(fig, filename='climate_change_scatter-and-line.html')

def getGlobalData():
    print("--- %s seconds --- Getting global data for scatterplot with fitted line" % (time.time() - start_time))
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
    print("--- %s seconds --- Getting country data for scatterplot with fitted line" % (time.time() - start_time))
    if os.path.isfile('data/r.csv'):
        df = pd.read_csv('data/df_highlow.csv')
    else:
        # Reading the dataset and storing it
        df = pd.read_csv('data/GlobalLandTemperaturesByCountry.csv')

        # Remove all empty elements
        df = df.dropna()

        # Cast string to datetime
        df['dt'] = pd.to_datetime(df['dt'], format='%Y-%m-%d')

        # Merge all monthly items to one year item
        df_max = df.groupby([pd.Grouper(key='dt', freq='1Y'), 'Country']).max().reset_index()
        df_min = df.groupby([pd.Grouper(key='dt', freq='1Y'), 'Country']).min().reset_index()

        df = df.groupby([pd.Grouper(key='dt', freq='1Y'), 'Country']).mean().reset_index()
        df['Max'] = df_max['AverageTemperature']
        df['Min'] = df_min['AverageTemperature']

        # Remove all dates not in scope
        years = list(range(1750, 2014))
        df = df[pd.DatetimeIndex(df['dt']).year.isin(years)]
        
        # Remove month and day from full date 
        df['dt'] = pd.DatetimeIndex(df['dt']).year
        df.to_csv('data/df_highlow.csv')

    return df

if __name__ == '__main__':
    country = 'Global'
    start = 1900
    end = 2015

    if country == 'Global':
        df = getGlobalData()
    else:
        df = getData()

    createScatter(df, country, start, end)
