from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go
import pandas as pd
from numpy import arange,array,ones
import os.path
import time
from scipy import stats

start_time = time.time()

def getGlobalDataByDateRange(co2, start = 1960, end = 2016):
    x = co2[(co2['Year'] > start) & (co2['Year'] <= end)]['Year']
    
    y_co2 = co2[(co2['Year'] > start) & (co2['Year'] <= end)]['Global']

    co2goal = float((co2[co2['Year'] == 1990]['Global']) / 2)

    print(co2goal)

    traceCO2 = go.Scatter(
                        x=x,
                        y=co2['Global'],
                        mode='lines',
                        marker=go.Marker(color='rgb(255, 153, 51)'),
                        name='CO₂ emmission'
                        )

    lineCO2 = go.Scatter(
                        x=x,
                        y=[co2goal] * len(x),
                        line = dict(
                            color = ('rgb(205, 12, 24)'),
                            width = 2,
                            dash = 'dot'),
                        name='CO₂ Goal'
                        )


    return [traceCO2, lineCO2]

def getFigure(co2, start = 1960, end = 2016):
    print("--- %s seconds --- Getting figure of scatterplot with fitted line" % (time.time() - start_time))

    data = getGlobalDataByDateRange(co2, start, end)
    
    layout = dict(title = 'Global - average MtCO₂ emmission between ' + str(start) + ' - ' + str(end),
                  xaxis = dict(title = 'Year -->'),
                  yaxis = dict(title = 'Emmission in MtCO₂ -->'),
                )

    return dict(data = data, layout = layout)

def createScatter(co2, start = 1960, end = 2016):
    print("--- %s seconds --- Plotting figure of scatterplot with fitted line" % (time.time() - start_time))
    fig = getFigure(co2, start, end)
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
    return df


if __name__ == '__main__':
    country = 'Global'
    start = 1960
    end = 2016

    co2 = getCO2Data()

    createScatter(co2, start, end)
