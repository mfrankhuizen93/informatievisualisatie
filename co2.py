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

def getData():
    print("--- %s seconds --- Getting CO2 emmission" % (time.time() - start_time))
    df = pd.read_csv('data/GlobalCarbonAtlas_territorial.csv', header=1)
    columns = list(df)[1:]
    df['Global'] = df[columns].mean(axis=1)
    return df


if __name__ == '__main__':
    country = 'Global'
    start = 1960
    end = 2016

    co2 = getData()

    createScatter(co2, start, end)
