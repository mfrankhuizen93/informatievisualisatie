from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go
import pandas as pd
from numpy import arange,array,ones
import os.path
import time
from scipy import stats

start_time = time.time()

def getGlobalDataByDateRange(df, co2, start = 1960, end = 2016):
    maxAllowed = df[df['dt'] == 1850]['LandAverageTemperature'] + 2

    y = df[(df['dt'] > start) & (df['dt'] <= end)]['LandAverageTemperature']
    x = df[(df['dt'] > start) & (df['dt'] <= end)]['dt']
    
    y_co2 = co2[(co2['Year'] > start) & (co2['Year'] <= end)]['Global']

    xi = arange(0, len(x))
        
    # Generated linear fit
    slope, intercept, _, _, _ = stats.linregress(xi, y)

    line = slope*xi+intercept


    co2goal = co2[co2['Year'] == 1960]['Global']

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

    traceCO2 = go.Scatter(
                        x=x,
                        y=co2['Global'],
                        mode='lines',
                        marker=go.Marker(color='rgb(255, 153, 51)'),
                        name='Fitted line'
                        name='MtCO₂/10 emmission'
                        )


    print([co2goal[0]] * len(x))
    lineCO2 = go.Scatter(
                        x=x,
                        y=[co2goal[0]] * len(x),
                        line = dict(
                            color = ('rgb(205, 12, 24)'),
                            width = 4,
                            dash = 'dot'),
                        name='MtCO₂/10 Goal'
                        )


    return [trace1, trace2, traceCO2, lineCO2]

def getFigure(df, co2, start = 1960, end = 2016):
    print("--- %s seconds --- Getting figure of scatterplot with fitted line" % (time.time() - start_time))

    data = getGlobalDataByDateRange(df, co2, start, end)
    
    layout = dict(title = 'Global - maximum, average and minimum temperature between ' + str(start) + ' - ' + str(end),
                  xaxis = dict(title = 'Year -->'),
                  yaxis = dict(title = 'Temperature in °C -->'),
                )

    return dict(data = data, layout = layout)

def createScatter(df, co2, start = 1960, end = 2016):
    print("--- %s seconds --- Plotting figure of scatterplot with fitted line" % (time.time() - start_time))
    fig = getFigure(df, co2, start, end)
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

        years = list(range(1960, 2016))
        df = df[pd.DatetimeIndex(df['dt']).year.isin(years)]

        # Remove month and day from full date 
        df['dt'] = pd.DatetimeIndex(df['dt']).year
        df.to_csv('data/df_global.csv')
    return df

def getCO2Data():
    print("--- %s seconds --- Getting CO2 emmission" % (time.time() - start_time))
    df = pd.read_csv('data/carbon/GlobalCarbonAtlas_territorial.csv', header=1)
    columns = list(df)[1:]
    df['Global'] = df[columns].mean(axis=1)
    print(df.head())
    return df


if __name__ == '__main__':
    country = 'Global'
    start = 1960
    end = 2016

    co2 = getCO2Data()
    df = getGlobalData()

    createScatter(df, co2, start, end)
