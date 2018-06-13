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

    # S & W krijgen een '-' voor de getal
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

    # Cast string to datetime
    gltByCity['dt'] = pd.to_datetime(gltByCity['dt'], format='%Y-%m-%d')
    print("--- %s seconds --- Converted dt to datetime" % (time.time() - start_time))

    # Merge all monthly items to one year item
    gltByCity = gltByCity.groupby(['City', 'Country', 'Longitude', 'Latitude', pd.Grouper(key='dt', freq='1Y')]).mean().reset_index()

    print("--- %s seconds --- Grouped all by one year" % (time.time() - start_time))

    # Remove all dates not in scope
    years = list(range(1750, 2014))
    gltByCity = gltByCity[pd.DatetimeIndex(gltByCity['dt']).year.isin(years)]
    print("--- %s seconds --- Removed all dates not in scope" % (time.time() - start_time))

    # Remove month and day from full date 
    gltByCity['dt'] = pd.DatetimeIndex(gltByCity['dt']).year
    print("--- %s seconds --- Removed month and day from full date" % (time.time() - start_time))

    df = gltByCity
    df.to_csv('data/df.csv')

    # createBubblemap(df)

if __name__ == '__main__':
    getData()
