from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os.path
import time

start_time = time.time()
gltCities = ""

def createBubblemap(df):
    print("--- %s seconds --- Started creating bubbleMap " % (time.time() - start_time))

    years = df['dt'].unique()
    temp = []

    # df['Hoverinfo'] = df['City'] + '<br>Average temperature ' + (df['AverageTemperature']).astype(str)+' degrees'

    a = dict(
        type = 'scattergeo',
        locationmode = 'world',
        lon = df[ (df['dt'] == 2010)]['Longitude'].str[:-1],
        lat = df[ (df['dt'] == 2010)]['Latitude'].str[:-1],
        text = df['City'] + '<br>Average temperature ' + (df['AverageTemperature']).astype(str)+' degrees',
        hoverinfo = 'text',
        marker = dict(
            size = df[ (df['dt'] == 2010)]['AverageTemperature'] * 10,
            color = df[ (df['dt'] == 2010)]['AverageTemperature'] * 10,
            line = dict(width=0.5, color='rgb(40,40,40)'),
            sizemode = 'area'
        ), 

        name = df[ (df['dt'] == 2010)]['City'] )

    temp.append(a)

    layout = dict(
            title = 'Titel hier',
            showlegend = True,
            geo = dict(
                projection=dict( type='natural earth' ),
                showland = True,
                landcolor = 'rgb(240, 240, 240)',
                subunitwidth=1,
                countrywidth=1,
                subunitcolor="rgb(245, 245, 245)",
                countrycolor="rgb(245, 245, 245)"
            ),
        )

    fig = dict( data=temp, layout=layout )
    plot(fig, filename='bubbleMap.html' )

def getData():
    # if os.path.isfile('data/df.csv'):
    #     df = pd.read_csv('data/df.csv')
    #     print("--- %s seconds --- Getting optimized dataset " % (time.time() - start_time))
    # else:
        # Reading the dataset and storing it
    gltByCity = pd.read_csv('data/GlobalLandTemperaturesByCity.csv')
    print("--- %s seconds --- Read dataset" % (time.time() - start_time))

    # Remove all empty elements
    gltByCity = gltByCity.dropna()
    print("--- %s seconds --- Dropped empty rows" % (time.time() - start_time))

    # Get all city names
    cities = gltByCity['City'].unique();
    print("--- %s seconds --- Got all city names" % (time.time() - start_time))



    years = list(range(2000, 2014))

    df = gltByCity.iloc[0:0]

    for city in cities:
        # for year in years:
        year = 2010
        print(city, year)
        temp = gltByCity[ (gltByCity['City'] == city) & (gltByCity['dt'].str.startswith(str(year))) ]

        if (temp.shape[0] > 0):
            df = df.append(temp.iloc[0])
            df.loc[df.index[-1], 'dt']= year
            averageTemperature = temp['AverageTemperature'].mean()
            uncertainty = temp['AverageTemperatureUncertainty'].mean()
            df.loc[df.index[-1], 'AverageTemperature']= averageTemperature
            df.loc[df.index[-1], 'AverageTemperatureUncertainty']= uncertainty

            df.to_csv('data/df.csv')
            print("--- {} seconds --- Added {} to csv".format(time.time() - start_time, city))

    print("--- %s seconds --- Casted dataset to dictionary" % (time.time() - start_time))
    df.to_csv('data/df.csv')

    createBubblemap(df)

if __name__ == '__main__':
    getData()
